"""
Fall Detection Android App — with SMS Alerts
Polls Railway API every 500ms, shows live status, sends SMS on fall.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex, platform
from kivy.metrics import dp
import threading
import requests
import json
from datetime import datetime

# ── Android SMS & GPS setup ──────────────────────────────────────────────────
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    
    # Request permissions on startup
    request_permissions([
        Permission.SEND_SMS,
        Permission.ACCESS_FINE_LOCATION,
        Permission.ACCESS_COARSE_LOCATION,
        Permission.INTERNET,
    ])
    
    def send_sms_android(phone_number, message):
        """Send SMS using Android SmsManager."""
        try:
            SmsManager = autoclass('android.telephony.SmsManager')
            sms = SmsManager.getDefault()
            if len(message) > 160:
                parts = sms.divideMessage(message)
                sms.sendMultipartTextMessage(phone_number, None, parts, None, None)
            else:
                sms.sendTextMessage(phone_number, None, message, None, None)
            return True
        except Exception as e:
            print(f"SMS error: {e}")
            return False
    
    def get_gps_location_android():
        """Get GPS location using Android LocationManager."""
        try:
            Context = autoclass('android.content.Context')
            LocationManager = autoclass('android.location.LocationManager')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            lm = activity.getSystemService(Context.LOCATION_SERVICE)
            
            for provider in ['gps', 'network']:
                try:
                    loc = lm.getLastKnownLocation(provider)
                    if loc:
                        return loc.getLatitude(), loc.getLongitude()
                except Exception:
                    continue
            return None, None
        except Exception as e:
            print(f"GPS error: {e}")
            return None, None
else:
    # PC testing stubs
    Window.size = (390, 844)
    def send_sms_android(phone, msg):
        print(f"[PC TEST] SMS to {phone}: {msg}")
        return True
    def get_gps_location_android():
        return 31.5204, 74.3587  # Lahore test coordinates

# ── Colours ──────────────────────────────────────────────────────────────────
C_BG        = get_color_from_hex('#0D1117')
C_CARD      = get_color_from_hex('#161B22')
C_GREEN     = get_color_from_hex('#2ECC71')
C_RED       = get_color_from_hex('#E74C3C')
C_ORANGE    = get_color_from_hex('#F39C12')
C_BLUE      = get_color_from_hex('#3498DB')
C_WHITE     = get_color_from_hex('#ECEFF4')
C_GREY      = get_color_from_hex('#8B949E')
C_DARK_CARD = get_color_from_hex('#21262D')

Window.clearcolor = C_BG

# ── Helpers ───────────────────────────────────────────────────────────────────
def card(widget, color=None):
    """Wrap a widget with a rounded card background."""
    color = color or C_CARD
    with widget.canvas.before:
        Color(*color)
        widget._rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(12)])
    widget.bind(pos=lambda w, v: setattr(w._rect, 'pos', v),
                size=lambda w, v: setattr(w._rect, 'size', v))
    return widget

def lbl(text, size=16, color=None, bold=False, halign='center'):
    color = color or C_WHITE
    l = Label(text=text, font_size=dp(size), color=color,
              bold=bold, halign=halign, valign='middle')
    l.bind(size=l.setter('text_size'))
    return l

def btn(text, bg_color=None, text_color=None, on_press=None, height=dp(50)):
    bg_color   = bg_color   or C_BLUE
    text_color = text_color or C_WHITE
    b = Button(text=text, font_size=dp(15), bold=True,
               color=text_color, background_normal='',
               background_color=bg_color, size_hint_y=None, height=height)
    if on_press:
        b.bind(on_press=on_press)
    return b

# ── Settings Screen ───────────────────────────────────────────────────────────
class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'settings'
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        layout.add_widget(lbl('Settings', size=22, bold=True))
        
        # Emergency Contact
        layout.add_widget(lbl('Emergency Contact Number', size=14, color=C_GREY, halign='left'))
        self.contact_input = TextInput(
            text=App.get_running_app().emergency_contact if App.get_running_app() else '',
            font_size=dp(16), multiline=False,
            size_hint_y=None, height=dp(48),
            background_color=C_DARK_CARD, foreground_color=C_WHITE,
            cursor_color=C_BLUE, hint_text='+923001234567'
        )
        layout.add_widget(self.contact_input)
        layout.add_widget(lbl('Format: +92xxxxxxxxxx', size=11, color=C_GREY, halign='left'))

        # Server URL (Editable)
        layout.add_widget(lbl('Server URL', size=14, color=C_GREY, halign='left'))
        self.url_input = TextInput(
            text=App.get_running_app().base_url if App.get_running_app() else '',
            font_size=dp(14), multiline=False,
            size_hint_y=None, height=dp(48),
            background_color=C_DARK_CARD, foreground_color=C_WHITE,
            cursor_color=C_BLUE, 
            hint_text='https://your-app.up.railway.app'
        )
        layout.add_widget(self.url_input)
        layout.add_widget(lbl('Railway or custom server URL', size=11, color=C_GREY, halign='left'))

        layout.add_widget(btn('Save Settings', bg_color=C_BLUE, on_press=self.save_settings))
        layout.add_widget(btn('Test Connection', bg_color=C_ORANGE, on_press=self.test_connection))
        layout.add_widget(btn('Test SMS', bg_color=C_ORANGE, on_press=self.test_sms))

        self.status_lbl = lbl('', size=13, color=C_GREY)
        layout.add_widget(self.status_lbl)
        
        layout.add_widget(btn('Back', bg_color=C_DARK_CARD, on_press=self._go_back))
        layout.add_widget(Label())  # spacer

        self.add_widget(layout)

    def save_settings(self, *_):
        app = App.get_running_app()
        app.emergency_contact = self.contact_input.text.strip()
        app.base_url = self.url_input.text.strip()
        self.status_lbl.text  = 'Settings saved!'
        self.status_lbl.color = C_GREEN

    def test_connection(self, *_):
        url = self.url_input.text.strip()
        if not url:
            self.status_lbl.text  = 'Enter server URL first'
            self.status_lbl.color = C_RED
            return
        
        def _test():
            try:
                r = requests.get(f"{url}/ping", timeout=5)
                d = r.json()
                Clock.schedule_once(lambda dt: self._set_status(
                    f"Connected! Model: {d.get('model','?')} ({d.get('accuracy',0)*100:.1f}%)", C_GREEN))
            except Exception as e:
                Clock.schedule_once(lambda dt: self._set_status(f"Connection failed: {str(e)[:30]}", C_RED))
        
        threading.Thread(target=_test, daemon=True).start()
        self.status_lbl.text  = 'Testing connection...'
        self.status_lbl.color = C_ORANGE

    def test_sms(self, *_):
        contact = self.contact_input.text.strip()
        if not contact:
            self.status_lbl.text  = 'Enter contact number first'
            self.status_lbl.color = C_RED
            return
        
        def _send():
            success = send_sms_android(contact, "Test message from Fall Guard app. SMS is working!")
            if success:
                Clock.schedule_once(lambda dt: self._set_status('Test SMS sent successfully!', C_GREEN))
            else:
                Clock.schedule_once(lambda dt: self._set_status('SMS send failed!', C_RED))
        
        threading.Thread(target=_send, daemon=True).start()
        self.status_lbl.text  = 'Sending test SMS...'
        self.status_lbl.color = C_ORANGE

    def _set_status(self, text, color):
        self.status_lbl.text  = text
        self.status_lbl.color = color

    def _go_back(self, *_):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current    = 'home'

# ── Home / Live Monitor Screen ────────────────────────────────────────────────
class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'home'
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))

        # Top bar
        top = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        top.add_widget(lbl('Fall Detection', size=20, bold=True, halign='left'))
        self.conn_dot = lbl('Offline', size=13, color=C_RED, halign='right')
        top.add_widget(self.conn_dot)
        root.add_widget(top)

        # Big status card
        self.status_card = BoxLayout(orientation='vertical', size_hint_y=None,
                                     height=dp(180), padding=dp(16), spacing=dp(8))
        card(self.status_card, C_DARK_CARD)

        self.status_icon  = lbl('O', size=48)
        self.status_label = lbl('NO FALL', size=28, bold=True, color=C_GREEN)
        self.prob_label   = lbl('Probability: -', size=14, color=C_GREY)
        self.conf_label   = lbl('Confidence: -', size=13, color=C_GREY)

        self.status_card.add_widget(self.status_icon)
        self.status_card.add_widget(self.status_label)
        self.status_card.add_widget(self.prob_label)
        self.status_card.add_widget(self.conf_label)
        root.add_widget(self.status_card)

        # Stats row
        stats = GridLayout(cols=3, size_hint_y=None, height=dp(90), spacing=dp(8))

        self.samples_card = self._stat_card('Samples', '0')
        self.falls_card   = self._stat_card('Falls', '0')
        self.time_card    = self._stat_card('Last Update', '-')

        stats.add_widget(self.samples_card[0])
        stats.add_widget(self.falls_card[0])
        stats.add_widget(self.time_card[0])
        root.add_widget(stats)

        # Probability bar
        bar_box = BoxLayout(orientation='vertical', size_hint_y=None,
                            height=dp(70), padding=dp(8), spacing=dp(4))
        card(bar_box)
        bar_box.add_widget(lbl('Fall Probability', size=12, color=C_GREY))

        self.prob_bar_bg = BoxLayout(size_hint_y=None, height=dp(20))
        with self.prob_bar_bg.canvas.before:
            Color(*C_DARK_CARD)
            self.prob_bar_bg._bg = RoundedRectangle(
                pos=self.prob_bar_bg.pos, size=self.prob_bar_bg.size, radius=[dp(6)])
        self.prob_bar_bg.bind(
            pos=lambda w, v: setattr(w._bg, 'pos', v),
            size=lambda w, v: setattr(w._bg, 'size', v))

        self.prob_bar_fill = BoxLayout(size_hint_x=0.0, size_hint_y=1)
        with self.prob_bar_fill.canvas.before:
            self._bar_color = Color(*C_GREEN)
            self.prob_bar_fill._fill = RoundedRectangle(
                pos=self.prob_bar_fill.pos, size=self.prob_bar_fill.size, radius=[dp(6)])
        self.prob_bar_fill.bind(
            pos=lambda w, v: setattr(w._fill, 'pos', v),
            size=lambda w, v: setattr(w._fill, 'size', v))

        self.prob_bar_bg.add_widget(self.prob_bar_fill)
        bar_box.add_widget(self.prob_bar_bg)
        root.add_widget(bar_box)

        # Recent events log
        log_box = BoxLayout(orientation='vertical', spacing=dp(6))
        log_box.add_widget(lbl('Recent Events', size=14, bold=True, halign='left'))

        scroll = ScrollView()
        self.log_layout = BoxLayout(orientation='vertical', spacing=dp(4),
                                    size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        scroll.add_widget(self.log_layout)
        log_box.add_widget(scroll)
        root.add_widget(log_box)

        # Bottom buttons
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        btns.add_widget(btn('Settings', bg_color=C_DARK_CARD, on_press=self._go_settings))
        btns.add_widget(btn('Reset', bg_color=C_DARK_CARD, on_press=self._reset))
        btns.add_widget(btn('History', bg_color=C_DARK_CARD, on_press=self._go_history))
        root.add_widget(btns)

        self.add_widget(root)

        # Internal state
        self._fall_count   = 0
        self._last_pred    = 0
        self._last_ts      = ''
        self._poll_event   = None

    def _stat_card(self, title, value):
        box = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(2))
        card(box)
        title_lbl = lbl(title, size=11, color=C_GREY)
        value_lbl = lbl(value, size=18, bold=True)
        box.add_widget(title_lbl)
        box.add_widget(value_lbl)
        return box, value_lbl

    def on_enter(self):
        if self._poll_event:
            self._poll_event.cancel()
        self._poll_event = Clock.schedule_interval(self._poll, 0.5)

    def on_leave(self):
        if self._poll_event:
            self._poll_event.cancel()

    def _poll(self, dt):
        threading.Thread(target=self._fetch_result, daemon=True).start()

    def _fetch_result(self):
        app = App.get_running_app()
        try:
            r = requests.get(f"{app.base_url}/result", timeout=2)
            data = r.json()
            Clock.schedule_once(lambda dt: self._update_ui(data))
        except Exception:
            Clock.schedule_once(lambda dt: self._set_offline())

    def _update_ui(self, data):
        pred  = data.get('prediction', 0)
        prob  = data.get('probability', 0.0)
        conf  = data.get('confidence', 'low')
        label = data.get('label', 'NO FALL')
        ts    = data.get('timestamp', '')
        total = data.get('total_samples', 0)

        # Connection status
        self.conn_dot.text  = 'Live'
        self.conn_dot.color = C_GREEN

        # Status card
        if pred == 1:
            self.status_icon.text   = 'X'
            self.status_label.text  = 'FALL DETECTED'
            self.status_label.color = C_RED
            card(self.status_card, get_color_from_hex('#2D1B1B'))

            # Send SMS on new fall (not repeat)
            if ts != self._last_ts:
                self._last_ts = ts
                self._fall_count += 1
                self.falls_card[1].text = str(self._fall_count)
                self._add_log_entry(f"FALL at {ts[11:19]}", C_RED)
                self._notify_fall(prob, ts)
        else:
            self.status_icon.text   = 'O'
            self.status_label.text  = 'NO FALL'
            self.status_label.color = C_GREEN
            card(self.status_card, C_DARK_CARD)

        self._last_pred = pred

        # Probability & confidence
        self.prob_label.text = f"Probability: {prob*100:.1f}%"
        conf_colors = {'high': C_GREEN, 'medium': C_ORANGE, 'low': C_RED}
        self.conf_label.text  = f"Confidence: {conf.upper()}"
        self.conf_label.color = conf_colors.get(conf, C_GREY)

        # Stats
        self.samples_card[1].text = str(total)
        try:
            self.time_card[1].text = ts[11:19]
        except Exception:
            pass

        # Probability bar
        self.prob_bar_fill.size_hint_x = min(1.0, prob)
        if prob > 0.7:
            self._bar_color.rgba = [*C_RED, 1]
        elif prob > 0.4:
            self._bar_color.rgba = [*C_ORANGE, 1]
        else:
            self._bar_color.rgba = [*C_GREEN, 1]

    def _set_offline(self):
        self.conn_dot.text  = 'Offline'
        self.conn_dot.color = C_RED

    def _add_log_entry(self, text, color=None):
        color = color or C_GREY
        entry = lbl(text, size=12, color=color, halign='left')
        entry.size_hint_y = None
        entry.height      = dp(28)
        self.log_layout.add_widget(entry, index=len(self.log_layout.children))
        if len(self.log_layout.children) > 30:
            self.log_layout.remove_widget(self.log_layout.children[-1])

    def _notify_fall(self, prob, timestamp):
        """Send SMS alert automatically on fall detection."""
        app = App.get_running_app()
        contact = app.emergency_contact.strip()
        
        if not contact:
            self._add_log_entry('No emergency contact set!', C_ORANGE)
            return
        
        # Try notification first
        try:
            from plyer import notification
            notification.notify(
                title='FALL DETECTED',
                message=f'Probability: {prob*100:.0f}%',
                app_name='Fall Guard',
                timeout=10
            )
        except Exception:
            pass
        
        # Send SMS in background
        threading.Thread(target=self._send_sms_alert,
                        args=(contact, prob, timestamp), daemon=True).start()

    def _send_sms_alert(self, contact, prob, timestamp):
        """Send SMS with GPS location."""
        lat, lng = get_gps_location_android()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if lat and lng:
            maps_url = f"https://maps.google.com/?q={lat},{lng}"
            msg = (f"FALL DETECTED!\n"
                   f"Time: {now}\n"
                   f"Prob: {prob*100:.0f}%\n"
                   f"Location: {maps_url}")
        else:
            msg = (f"FALL DETECTED!\n"
                   f"Time: {now}\n"
                   f"Prob: {prob*100:.0f}%\n"
                   f"GPS unavailable")
        
        success = send_sms_android(contact, msg)
        
        if success:
            Clock.schedule_once(lambda dt: self._add_log_entry(
                f"SMS sent to {contact[-4:].rjust(len(contact),'*')}", C_GREEN))
        else:
            Clock.schedule_once(lambda dt: self._add_log_entry(
                'SMS send failed', C_RED))

    def _reset(self, *_):
        app = App.get_running_app()
        def _do():
            try:
                requests.post(f"{app.base_url}/reset", timeout=2)
                Clock.schedule_once(lambda dt:
                    self._add_log_entry('Buffer reset', C_BLUE))
            except Exception:
                pass
        threading.Thread(target=_do, daemon=True).start()

    def _go_settings(self, *_):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current    = 'settings'

    def _go_history(self, *_):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current    = 'history'

# ── History Screen ────────────────────────────────────────────────────────────
class HistoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'history'
        layout = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))

        top = BoxLayout(size_hint_y=None, height=dp(50))
        top.add_widget(lbl('Fall History', size=20, bold=True, halign='left'))
        top.add_widget(btn('Back', bg_color=C_DARK_CARD,
                           on_press=self._go_back, height=dp(40)))
        layout.add_widget(top)

        self.refresh_btn = btn('Refresh', bg_color=C_BLUE,
                               on_press=self._load_history)
        layout.add_widget(self.refresh_btn)

        scroll = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', spacing=dp(6),
                                        size_hint_y=None, padding=dp(4))
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def on_enter(self):
        self._load_history()

    def _load_history(self, *_):
        app = App.get_running_app()
        def _fetch():
            try:
                r    = requests.get(f"{app.base_url}/history", timeout=3)
                data = r.json()
                Clock.schedule_once(lambda dt: self._show_history(data.get('falls', [])))
            except Exception as e:
                Clock.schedule_once(lambda dt: self._show_error(str(e)))
        threading.Thread(target=_fetch, daemon=True).start()

    def _show_history(self, falls):
        self.history_layout.clear_widgets()
        if not falls:
            self.history_layout.add_widget(
                lbl('No fall events recorded yet.', color=C_GREY))
            return
        for event in reversed(falls):
            row = BoxLayout(size_hint_y=None, height=dp(56),
                            padding=dp(10), spacing=dp(8))
            card(row, get_color_from_hex('#2D1B1B'))
            row.add_widget(lbl('X', size=22, halign='left'))
            info = BoxLayout(orientation='vertical')
            info.add_widget(lbl('FALL DETECTED', size=14, bold=True,
                                color=C_RED, halign='left'))
            info.add_widget(lbl(f"{event.get('time','?')}  |  "
                                f"Prob: {event.get('probability',0)*100:.0f}%",
                                size=11, color=C_GREY, halign='left'))
            row.add_widget(info)
            self.history_layout.add_widget(row)

    def _show_error(self, msg):
        self.history_layout.clear_widgets()
        self.history_layout.add_widget(lbl(f'Error: {msg}', color=C_RED))

    def _go_back(self, *_):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current    = 'home'

# ── App ───────────────────────────────────────────────────────────────────────
class FallDetectionApp(App):
    base_url = 'https://web-production-2755d.up.railway.app'
    emergency_contact = ''  # User sets in Settings

    def build(self):
        self.title = 'Fall Guard'
        sm = ScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(SettingsScreen())
        sm.add_widget(HistoryScreen())
        sm.current = 'home'
        return sm

if __name__ == '__main__':
    FallDetectionApp().run()
