"""
Fall Guard — Professional Fall Detection App
Ultra-modern dark UI with glassmorphism cards
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import (Color, RoundedRectangle, Rectangle,
                            Ellipse, Line, SmoothLine)
from kivy.utils import get_color_from_hex, platform
from kivy.metrics import dp, sp
from kivy.animation import Animation
import threading, requests, json, os
from datetime import datetime

# ── Register bundled fonts ────────────────────────────────────────────────────
from kivy.core.text import LabelBase

try:
    LabelBase.register(name='Icons', fn_regular='assets/fonts/materialdesignicons-webfont.ttf')
    LabelBase.register(name='Inter', fn_regular='assets/fonts/Inter-Regular.ttf', fn_bold='assets/fonts/Inter-Bold.ttf')
    FONTS_AVAILABLE = True
except Exception as e:
    print(f"Font loading warning: {e}")
    FONTS_AVAILABLE = False

# Material Design Icons mapping
ICONS = {
    'shield': '\uF0785', 'settings': '\uF0493', 'chart': '\uF0127',
    'alert': '\uF0026', 'clock': '\uF0954', 'reset': '\uF0450',
    'history': '\uF02D7', 'phone': '\uF03CF', 'server': '\uF0484',
    'info': '\uF02FC', 'check': '\uF012C',
}

def icon_text(name):
    """Get icon glyph or fallback text"""
    if FONTS_AVAILABLE:
        return ICONS.get(name, '?')
    # Fallback text labels
    fallback = {
        'shield': '[*]', 'settings': '[S]', 'chart': '[#]',
        'alert': '[!]', 'clock': '[T]', 'reset': '[R]',
        'history': '[H]', 'phone': '[P]', 'server': '[>]',
        'info': '[i]', 'check': '[✓]',
    }
    return fallback.get(name, '[?]')

# ── Android setup ─────────────────────────────────────────────────────────────
if platform == 'android':
    from android.runnable import run_on_ui_thread  # noqa
    from android.permissions import request_permissions, Permission  # noqa
    from jnius import autoclass                    # noqa

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    View           = autoclass('android.view.View')
    WindowManager  = autoclass('android.view.WindowManager$LayoutParams')

    # Request all needed permissions on startup
    request_permissions([
        Permission.SEND_SMS,
        Permission.ACCESS_FINE_LOCATION,
        Permission.ACCESS_COARSE_LOCATION,
        Permission.VIBRATE,
        Permission.INTERNET,
    ])

    @run_on_ui_thread
    def _set_fullscreen(*args):
        activity = PythonActivity.mActivity
        win      = activity.getWindow()
        win.addFlags(WindowManager.FLAG_FULLSCREEN)
        decorView = win.getDecorView()
        flags = (View.SYSTEM_UI_FLAG_LAYOUT_STABLE
               | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
               | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
               | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
               | View.SYSTEM_UI_FLAG_FULLSCREEN
               | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
        decorView.setSystemUiVisibility(flags)

    Clock.schedule_once(_set_fullscreen, 0)
    Clock.schedule_once(_set_fullscreen, 1)

    def send_sms_android(phone_number, message):
        """Send SMS silently in background using Android SmsManager."""
        try:
            SmsManager = autoclass('android.telephony.SmsManager')
            sms = SmsManager.getDefault()
            # Split long messages automatically
            if len(message) > 160:
                parts = sms.divideMessage(message)
                sms.sendMultipartTextMessage(phone_number, None, parts,
                                             None, None)
            else:
                sms.sendTextMessage(phone_number, None, message, None, None)
            return True
        except Exception as e:
            print(f"SMS error: {e}")
            return False

    def get_gps_location_android():
        """Get GPS location using Android LocationManager."""
        try:
            Context        = autoclass('android.content.Context')
            LocationManager = autoclass('android.location.LocationManager')
            activity       = PythonActivity.mActivity
            lm = activity.getSystemService(Context.LOCATION_SERVICE)

            # Try GPS first, then network
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
    Window.size = (390, 844)

    def send_sms_android(phone, msg):
        print(f"[PC TEST] SMS to {phone}: {msg}")
        return True

    def get_gps_location_android():
        # Return test coordinates for PC testing
        return 31.5204, 74.3587  # Lahore coordinates

Window.clearcolor = get_color_from_hex('#060B18')

CLOUD_URL = 'https://web-production-44fc6.up.railway.app'

# ── Premium color palette ─────────────────────────────────────────────────────
C = {
    'bg'       : get_color_from_hex('#060B18'),
    'bg2'      : get_color_from_hex('#0D1526'),
    'surface'  : get_color_from_hex('#111827'),
    'card'     : get_color_from_hex('#161F35'),
    'card2'    : get_color_from_hex('#1C2840'),
    'border'   : get_color_from_hex('#1E3A5F'),
    'blue'     : get_color_from_hex('#3B82F6'),
    'blue2'    : get_color_from_hex('#60A5FA'),
    'cyan'     : get_color_from_hex('#06B6D4'),
    'green'    : get_color_from_hex('#10B981'),
    'green2'   : get_color_from_hex('#34D399'),
    'red'      : get_color_from_hex('#EF4444'),
    'red2'     : get_color_from_hex('#FCA5A5'),
    'orange'   : get_color_from_hex('#F59E0B'),
    'orange2'  : get_color_from_hex('#FCD34D'),
    'purple'   : get_color_from_hex('#8B5CF6'),
    'white'    : get_color_from_hex('#F8FAFC'),
    'white2'   : get_color_from_hex('#CBD5E1'),
    'grey'     : get_color_from_hex('#64748B'),
    'grey2'    : get_color_from_hex('#334155'),
    'dark_red' : get_color_from_hex('#1A0A0A'),
    'dark_grn' : get_color_from_hex('#0A1A12'),
    'dark_org' : get_color_from_hex('#1A1200'),
}

# ── Base widgets ──────────────────────────────────────────────────────────────
class GlassCard(BoxLayout):
    """Glassmorphism-style card with gradient border"""
    def __init__(self, bg=None, radius=16, border=True, **kw):
        super().__init__(**kw)
        self._bg     = bg or C['card']
        self._radius = radius
        self._border = border
        self._draw()
        self.bind(pos=self._redraw, size=self._redraw)

    def _draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            if self._border:
                Color(*C['border'])
                RoundedRectangle(pos=self.pos, size=self.size,
                                 radius=[dp(self._radius + 1)])
            Color(*self._bg)
            self._rect = RoundedRectangle(pos=(self.x+1, self.y+1),
                                          size=(self.width-2, self.height-2),
                                          radius=[dp(self._radius)])

    def _redraw(self, *_):
        self._draw()

    def update_bg(self, color):
        self._bg = color
        self._redraw()


def txt(text, size=14, color=None, bold=False,
        halign='center', italic=False, **kw):
    color = color or C['white']
    l = Label(text=text, font_size=sp(size), color=color,
              bold=bold, italic=italic, halign=halign,
              valign='middle', markup=True, **kw)
    l.bind(size=l.setter('text_size'))
    return l


def pill_btn(label, bg=None, fg=None, cb=None, r=12, **kw):
    bg = bg or C['blue']
    fg = fg or C['white']
    b  = Button(text=label, font_size=sp(14), bold=True,
                color=fg, background_normal='',
                background_color=(0, 0, 0, 0), **kw)
    with b.canvas.before:
        Color(*bg)
        b._r = RoundedRectangle(pos=b.pos, size=b.size, radius=[dp(r)])
    b.bind(pos=lambda w, v: setattr(w._r, 'pos', v),
           size=lambda w, v: setattr(w._r, 'size', v))
    if cb:
        b.bind(on_press=cb)
    return b


def divider():
    d = BoxLayout(size_hint_y=None, height=dp(1))
    with d.canvas:
        Color(*C['border'])
        Rectangle(pos=d.pos, size=d.size)
    d.bind(pos=lambda w, v: w.canvas.clear() or
           setattr(w, '_drawn', _draw_div(w)),
           size=lambda w, v: w.canvas.clear() or
           setattr(w, '_drawn', _draw_div(w)))
    return d


def _draw_div(w):
    with w.canvas:
        Color(*C['border'])
        Rectangle(pos=w.pos, size=w.size)

# ── Splash Screen ─────────────────────────────────────────────────────────────
class SplashScreen(Screen):
    def __init__(self, **kw):
        super().__init__(name='splash', **kw)
        fl = FloatLayout()
        with fl.canvas.before:
            Color(*C['bg'])
            self._bg = Rectangle(pos=fl.pos, size=fl.size)
        fl.bind(pos=lambda w, v: setattr(self._bg, 'pos', v),
                size=lambda w, v: setattr(self._bg, 'size', v))

        # Outer glow ring
        ring = FloatLayout(size_hint=(None, None), size=(dp(160), dp(160)),
                           pos_hint={'center_x': .5, 'center_y': .58})
        with ring.canvas:
            Color(*C['blue'], .15)
            Ellipse(pos=(0, 0), size=(dp(160), dp(160)))
            Color(*C['blue'], .3)
            Ellipse(pos=(dp(15), dp(15)), size=(dp(130), dp(130)))
            Color(*C['card'])
            Ellipse(pos=(dp(25), dp(25)), size=(dp(110), dp(110)))
        fl.add_widget(ring)

        # Icon
        icon_lbl = Label(text=icon_text('shield'), font_name='Icons' if FONTS_AVAILABLE else 'Roboto',
                         font_size=sp(46),
                         size_hint=(None, None), size=(dp(60), dp(60)),
                         pos_hint={'center_x': .5, 'center_y': .585})
        fl.add_widget(icon_lbl)

        # App name
        fl.add_widget(txt('[b]FALL[/b] [color=#3B82F6]GUARD[/color]',
                          size=28, size_hint=(1, None), height=dp(40),
                          pos_hint={'center_x': .5, 'y': .38}))

        fl.add_widget(txt('AI-Powered Fall Detection System',
                          size=13, color=C['grey'],
                          size_hint=(1, None), height=dp(28),
                          pos_hint={'center_x': .5, 'y': .32}))

        # Version badge
        badge = GlassCard(bg=C['card2'], radius=20, border=True,
                          size_hint=(None, None), size=(dp(160), dp(32)),
                          pos_hint={'center_x': .5, 'y': .22},
                          padding=[dp(12), dp(4)])
        badge.add_widget(txt('v1.0  •  97.98% Accuracy',
                             size=11, color=C['blue2']))
        fl.add_widget(badge)

        # Loading dots
        self._dot_lbl = txt('● ● ●', size=10, color=C['grey2'],
                            size_hint=(1, None), height=dp(20),
                            pos_hint={'center_x': .5, 'y': .12})
        fl.add_widget(self._dot_lbl)

        self.add_widget(fl)
        Clock.schedule_interval(self._animate_dots, 0.4)
        Clock.schedule_once(self._go, 3.0)
        self._dot_state = 0

    def _animate_dots(self, dt):
        states = ['●  ○  ○', '●  ●  ○', '●  ●  ●', '○  ●  ●',
                  '○  ○  ●', '○  ○  ○']
        self._dot_lbl.text = states[self._dot_state % len(states)]
        self._dot_state += 1

    def _go(self, *_):
        self.manager.current = 'home'

# ── Home Screen ───────────────────────────────────────────────────────────────
class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(name='home', **kw)
        self._fall_count = 0
        self._last_ts    = ''
        self._log_items  = []
        self._poll_ev    = None
        self._pulse_anim = None
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical',
                         padding=[dp(16), dp(12), dp(16), dp(12)],
                         spacing=dp(10))
        with root.canvas.before:
            Color(*C['bg'])
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda w, v: setattr(self._bg, 'pos', v),
                  size=lambda w, v: setattr(self._bg, 'size', v))

        # ── Header ────────────────────────────────────────────────────────────
        hdr = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(10))

        left = BoxLayout(orientation='vertical', spacing=dp(2))
        left.add_widget(txt('[b]Fall Guard[/b]', size=20,
                            color=C['white'], halign='left'))
        self._conn = txt('● Connecting...', size=11,
                         color=C['orange'], halign='left')
        left.add_widget(self._conn)
        hdr.add_widget(left)

        hdr.add_widget(BoxLayout())  # spacer

        # Settings button
        hdr.add_widget(pill_btn(icon_text('settings'), bg=C['card2'], r=10,
                                size_hint=(None, None), size=(dp(42), dp(42)),
                                cb=lambda _: setattr(self.manager, 'current', 'settings')))
        root.add_widget(hdr)

        # ── Main status card ──────────────────────────────────────────────────
        self._status_card = GlassCard(bg=C['card'], radius=24,
                                      orientation='vertical',
                                      size_hint_y=None, height=dp(210),
                                      padding=[dp(20), dp(16)], spacing=dp(4))

        # Top row: icon + label
        top_row = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(12))

        # Animated circle indicator
        self._ind = FloatLayout(size_hint=(None, 1), width=dp(70))
        with self._ind.canvas:
            Color(*C['green'], .15)
            self._ind_outer = Ellipse(pos=(0, dp(5)),
                                      size=(dp(60), dp(60)))
            Color(*C['green'], .4)
            self._ind_mid   = Ellipse(pos=(dp(8), dp(13)),
                                      size=(dp(44), dp(44)))
            Color(*C['green'])
            self._ind_inner = Ellipse(pos=(dp(16), dp(21)),
                                      size=(dp(28), dp(28)))
        top_row.add_widget(self._ind)

        status_txt_box = BoxLayout(orientation='vertical', spacing=dp(2))
        self._status_main = txt('[b]NO FALL[/b]', size=22,
                                color=C['green'], halign='left')
        self._status_sub  = txt('System monitoring active',
                                size=12, color=C['grey'], halign='left')
        status_txt_box.add_widget(self._status_main)
        status_txt_box.add_widget(self._status_sub)
        top_row.add_widget(status_txt_box)
        self._status_card.add_widget(top_row)

        # Probability row
        self._prob_lbl = txt('Fall Probability: —', size=12,
                             color=C['grey2'], halign='left',
                             size_hint_y=None, height=dp(20))
        self._status_card.add_widget(self._prob_lbl)

        # Progress bar
        bar_bg = GlassCard(bg=C['card2'], radius=8, border=False,
                           size_hint_y=None, height=dp(10))
        self._bar_fill = BoxLayout(size_hint_x=0.0, size_hint_y=1)
        with self._bar_fill.canvas.before:
            self._bar_col = Color(*C['green'])
            self._bar_fill._r = RoundedRectangle(
                pos=self._bar_fill.pos, size=self._bar_fill.size,
                radius=[dp(8)])
        self._bar_fill.bind(
            pos=lambda w, v: setattr(w._r, 'pos', v),
            size=lambda w, v: setattr(w._r, 'size', v))
        bar_bg.add_widget(self._bar_fill)
        self._status_card.add_widget(bar_bg)

        # Confidence + buffer row
        meta_row = BoxLayout(size_hint_y=None, height=dp(24),
                             spacing=dp(8))
        self._conf_lbl = txt('Confidence: —', size=11,
                             color=C['grey'], halign='left')
        self._buf_lbl  = txt('Buffer: 0/125', size=11,
                             color=C['grey'], halign='right')
        meta_row.add_widget(self._conf_lbl)
        meta_row.add_widget(self._buf_lbl)
        self._status_card.add_widget(meta_row)

        # Last update
        self._upd_lbl = txt('Last update: —', size=10,
                            color=C['grey2'], halign='right',
                            size_hint_y=None, height=dp(18))
        self._status_card.add_widget(self._upd_lbl)

        root.add_widget(self._status_card)

        # ── Stats row ─────────────────────────────────────────────────────────
        stats = GridLayout(cols=3, size_hint_y=None, height=dp(82),
                           spacing=dp(8))
        self._v_samples = self._stat(stats, icon_text('chart'), 'Samples', '0', C['blue2'])
        self._v_falls   = self._stat(stats, icon_text('alert'), 'Falls',   '0', C['red'])
        self._v_uptime  = self._stat(stats, icon_text('clock'), 'Uptime',  '0s', C['cyan'])
        root.add_widget(stats)

        # ── Quick actions ─────────────────────────────────────────────────────
        acts = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        acts.add_widget(pill_btn(f'{icon_text("reset")}  Reset Buffer', bg=C['card2'], r=10,
                                 cb=self._reset))
        acts.add_widget(pill_btn(f'{icon_text("history")}  History', bg=C['card2'], r=10,
                                 cb=lambda _: setattr(self.manager,
                                                      'current', 'history')))
        root.add_widget(acts)

        # ── Event log ─────────────────────────────────────────────────────────
        log_card = GlassCard(bg=C['card'], radius=16,
                             orientation='vertical',
                             padding=[dp(14), dp(10)], spacing=dp(6))

        log_hdr = BoxLayout(size_hint_y=None, height=dp(28))
        log_hdr.add_widget(txt('⚡  Live Events', size=13, bold=True,
                               color=C['white2'], halign='left'))
        self._log_count = txt('0 events', size=11, color=C['grey'],
                              halign='right')
        log_hdr.add_widget(self._log_count)
        log_card.add_widget(log_hdr)

        scroll = ScrollView(size_hint_y=1)
        self._log_box = BoxLayout(orientation='vertical', spacing=dp(5),
                                  size_hint_y=None)
        self._log_box.bind(minimum_height=self._log_box.setter('height'))
        scroll.add_widget(self._log_box)
        log_card.add_widget(scroll)
        root.add_widget(log_card)

        self.add_widget(root)
        self._start_time = datetime.now()

    def _stat(self, parent, icon, title, val, color):
        card = GlassCard(bg=C['card'], radius=12,
                         orientation='vertical',
                         padding=[dp(10), dp(8)], spacing=dp(2))
        card.add_widget(txt(icon, size=18, size_hint_y=None, height=dp(26)))
        v = txt(val, size=16, bold=True, color=color,
                size_hint_y=None, height=dp(24))
        card.add_widget(v)
        card.add_widget(txt(title, size=10, color=C['grey'],
                            size_hint_y=None, height=dp(16)))
        parent.add_widget(card)
        return v

    def on_enter(self):
        if self._poll_ev:
            self._poll_ev.cancel()
        self._poll_ev = Clock.schedule_interval(self._poll, 0.5)
        Clock.schedule_interval(self._update_uptime, 1)

    def on_leave(self):
        if self._poll_ev:
            self._poll_ev.cancel()

    def _update_uptime(self, dt):
        secs = int((datetime.now() - self._start_time).total_seconds())
        if secs < 60:
            self._v_uptime.text = f"{secs}s"
        else:
            self._v_uptime.text = f"{secs//60}m{secs%60}s"

    def _poll(self, dt):
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            import urllib.request, json as _j, ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            r = urllib.request.urlopen(
                f"{App.get_running_app().base_url}/result",
                timeout=5, context=ctx)
            Clock.schedule_once(lambda dt: self._update(_j.loads(r.read().decode())))
        except Exception as e:
            print(f"Fetch error: {e}")
            Clock.schedule_once(lambda dt: self._offline())
        except Exception:
            Clock.schedule_once(lambda dt: self._offline())

    def _update(self, d):
        pred   = d.get('prediction', 0)
        prob   = d.get('probability', 0.0)
        conf   = d.get('confidence', 'low')
        total  = d.get('total_samples', 0)
        ts     = d.get('timestamp', '')
        status = d.get('status', 'waiting')

        self._conn.text  = '●  Live'
        self._conn.color = C['green']
        self._v_samples.text = f"{total:,}"
        self._buf_lbl.text   = f"Buffer: {min(total,125)}/125"
        try:
            self._upd_lbl.text = f"Last update: {ts[11:19]}"
        except Exception:
            pass

        if status in ('waiting', 'collecting') and total < 125:
            self._set_state('collecting', prob)
            return

        if pred == 1:
            self._set_state('fall', prob)
            if ts != self._last_ts:
                self._last_ts = ts
                self._fall_count += 1
                self._v_falls.text = str(self._fall_count)
                self._add_log(f"🚨  FALL  {ts[11:19]}  —  {prob*100:.0f}%",
                              C['red'], C['dark_red'])
                self._notify(prob)
        else:
            self._set_state('safe', prob)

        # Confidence
        cc = {'high': C['green2'], 'medium': C['orange2'],
              'low': C['red2']}.get(conf, C['grey'])
        self._conf_lbl.text  = f"Confidence: {conf.upper()}"
        self._conf_lbl.color = cc

        # Prob bar
        self._bar_fill.size_hint_x = min(1.0, max(0.0, prob))
        if prob > 0.65:
            self._bar_col.rgba = [*C['red'], 1]
        elif prob > 0.4:
            self._bar_col.rgba = [*C['orange'], 1]
        else:
            self._bar_col.rgba = [*C['green'], 1]

        self._prob_lbl.text = f"Fall Probability: {prob*100:.1f}%"

    def _set_state(self, state, prob):
        if state == 'fall':
            self._status_main.text  = '[b]FALL DETECTED[/b]'
            self._status_main.color = C['red']
            self._status_sub.text   = '⚠  Immediate attention required!'
            self._status_sub.color  = C['red2']
            self._status_card.update_bg(C['dark_red'])
            self._set_indicator(C['red'])
        elif state == 'collecting':
            self._status_main.text  = '[b]Collecting...[/b]'
            self._status_main.color = C['orange']
            self._status_sub.text   = 'Filling sensor buffer'
            self._status_sub.color  = C['orange2']
            self._status_card.update_bg(C['card'])
            self._set_indicator(C['orange'])
        else:
            self._status_main.text  = '[b]NO FALL[/b]'
            self._status_main.color = C['green']
            self._status_sub.text   = 'System monitoring active'
            self._status_sub.color  = C['grey']
            self._status_card.update_bg(C['card'])
            self._set_indicator(C['green'])

    def _set_indicator(self, color):
        self._ind.canvas.clear()
        with self._ind.canvas:
            Color(*color, .15)
            Ellipse(pos=(0, dp(5)), size=(dp(60), dp(60)))
            Color(*color, .4)
            Ellipse(pos=(dp(8), dp(13)), size=(dp(44), dp(44)))
            Color(*color)
            Ellipse(pos=(dp(16), dp(21)), size=(dp(28), dp(28)))

    def _offline(self):
        self._conn.text  = '●  Offline'
        self._conn.color = C['red']

    def _add_log(self, text, fg, bg):
        row = GlassCard(bg=bg, radius=10, border=False,
                        size_hint_y=None, height=dp(38),
                        padding=[dp(10), dp(4)])
        row.add_widget(txt(text, size=12, color=fg, halign='left'))
        self._log_box.add_widget(row, index=len(self._log_box.children))
        if len(self._log_box.children) > 25:
            self._log_box.remove_widget(self._log_box.children[-1])
        self._log_count.text = f"{len(self._log_box.children)} events"

    def _notify(self, prob):
        """Fire notification + send WhatsApp automatically."""
        try:
            from plyer import notification
            notification.notify(title='FALL DETECTED',
                                message=f'Probability: {prob*100:.0f}%',
                                app_name='Fall Guard', timeout=10)
        except Exception:
            pass
        threading.Thread(target=self._send_sms_alert,
                         args=(prob,), daemon=True).start()

    def _send_sms_alert(self, prob):
        """Send SMS emergency alert automatically"""
        app   = App.get_running_app()
        phone = app.emergency_contact.strip()

        if not phone:
            Clock.schedule_once(lambda dt: self._add_log(
                'No emergency contact set!', C['orange'], C['dark_org']))
            return

        lat, lng = get_gps_location_android()
        now      = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

        # Send SMS automatically
        success = send_sms_android(phone, msg)
        
        if success:
            Clock.schedule_once(lambda dt: self._add_log(
                f"SMS sent to {phone[-4:].rjust(len(phone),'*')}",
                C['green'], C['dark_grn']))
        else:
            Clock.schedule_once(lambda dt: self._add_log(
                'SMS send failed', C['red'], C['dark_red']))

    def _reset(self, *_):
        def _do():
            try:
                import urllib.request, ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                urllib.request.urlopen(
                    urllib.request.Request(
                        f"{App.get_running_app().base_url}/reset",
                        method='POST'), timeout=3, context=ctx)
                Clock.schedule_once(lambda dt: self._add_log(
                    '🔄  Buffer reset', C['blue2'], C['card2']))
            except Exception:
                pass
        threading.Thread(target=_do, daemon=True).start()


# ── Settings Screen ───────────────────────────────────────────────────────────
class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(name='settings', **kw)
        root = BoxLayout(orientation='vertical',
                         padding=[dp(16), dp(12), dp(16), dp(12)],
                         spacing=dp(12))
        with root.canvas.before:
            Color(*C['bg'])
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda w, v: setattr(self._bg, 'pos', v),
                  size=lambda w, v: setattr(self._bg, 'size', v))

        # Header
        hdr = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(10))
        hdr.add_widget(pill_btn('←', bg=C['card2'], r=10,
                                size_hint=(None, None), size=(dp(42), dp(42)),
                                cb=lambda _: setattr(self.manager,
                                                     'current', 'home')))
        hdr.add_widget(txt('[b]Settings[/b]', size=20,
                           color=C['white'], halign='left'))
        root.add_widget(hdr)

        # Server card
        srv = GlassCard(bg=C['card'], radius=16, orientation='vertical',
                        size_hint_y=None, height=dp(230),
                        padding=dp(16), spacing=dp(10))

        srv.add_widget(txt('🌐  Server Configuration', size=13, bold=True,
                           color=C['blue2'], halign='left',
                           size_hint_y=None, height=dp(24)))
        srv.add_widget(txt('Cloud URL or PC IP Address', size=11,
                           color=C['grey'], halign='left',
                           size_hint_y=None, height=dp(18)))

        self._ip = TextInput(
            text='web-production-44fc6.up.railway.app',
            font_size=sp(12), multiline=False,
            size_hint_y=None, height=dp(44),
            background_color=C['card2'],
            foreground_color=C['white'],
            cursor_color=C['blue'],
            hint_text='e.g. web-xxx.up.railway.app',
            padding=[dp(12), dp(10)]
        )
        srv.add_widget(self._ip)

        srv.add_widget(txt('Port  (local only — ignored for cloud)',
                           size=11, color=C['grey'], halign='left',
                           size_hint_y=None, height=dp(18)))

        self._port = TextInput(
            text='5000', font_size=sp(12), multiline=False,
            size_hint_y=None, height=dp(44),
            background_color=C['card2'],
            foreground_color=C['white'],
            cursor_color=C['blue'],
            padding=[dp(12), dp(10)]
        )
        srv.add_widget(self._port)

        tog = BoxLayout(size_hint_y=None, height=dp(42))
        tog.add_widget(txt('☁  Use Cloud (HTTPS)', size=13,
                           color=C['white'], halign='left'))
        self._sw = Switch(active=True, size_hint=(None, None),
                          size=(dp(60), dp(40)))
        tog.add_widget(self._sw)
        srv.add_widget(tog)
        root.add_widget(srv)

        # Buttons
        # Emergency contact card
        emg = GlassCard(bg=C['card'], radius=16, orientation='vertical',
                        size_hint_y=None, height=dp(120),
                        padding=dp(16), spacing=dp(8))

        emg.add_widget(txt(f'{icon_text("phone")}  Emergency Contact (SMS)', size=13, bold=True,
                           color=C['red'], halign='left',
                           size_hint_y=None, height=dp(24)))

        emg.add_widget(txt('Phone number with country code (e.g. 923001234567)',
                           size=11, color=C['grey'], halign='left',
                           size_hint_y=None, height=dp(18)))

        self._emg = TextInput(
            text='',
            font_size=sp(14), multiline=False,
            size_hint_y=None, height=dp(44),
            background_color=C['card2'],
            foreground_color=C['white'],
            cursor_color=C['red'],
            hint_text='e.g. 923001234567',
            input_filter='int',
            padding=[dp(12), dp(10)]
        )
        emg.add_widget(self._emg)
        root.add_widget(emg)

        root.add_widget(pill_btn('💾  Save & Connect', bg=C['blue'], r=12,
                                 size_hint_y=None, height=dp(50),
                                 cb=self._save))
        root.add_widget(pill_btn('🔗  Test Connection', bg=C['card2'], r=12,
                                 size_hint_y=None, height=dp(50),
                                 cb=self._test))

        self._status = txt('', size=12, color=C['grey'],
                           size_hint_y=None, height=dp(28))
        root.add_widget(self._status)

        # Model info card
        info = GlassCard(bg=C['card'], radius=16, orientation='vertical',
                         size_hint_y=None, height=dp(120),
                         padding=dp(16), spacing=dp(6))
        info.add_widget(txt('🤖  Model Information', size=13, bold=True,
                            color=C['purple'], halign='left',
                            size_hint_y=None, height=dp(24)))
        for line in [
            ('Algorithm', 'Gradient Boosting'),
            ('Accuracy',  '97.98%'),
            ('Window',    '125 samples  (2.5 seconds)'),
            ('Threshold', '0.60  (60% probability)'),
        ]:
            row = BoxLayout(size_hint_y=None, height=dp(18))
            row.add_widget(txt(line[0], size=11, color=C['grey'],
                               halign='left'))
            row.add_widget(txt(line[1], size=11, color=C['white2'],
                               halign='right'))
            info.add_widget(row)
        root.add_widget(info)

        root.add_widget(BoxLayout())  # spacer
        self.add_widget(root)

    def _save(self, *_):
        app = App.get_running_app()
        ip  = self._ip.text.strip()
        if self._sw.active:
            app.base_url = f"https://{ip}"
        else:
            app.base_url = f"http://{ip}:{self._port.text.strip()}"
        app.emergency_contact = self._emg.text.strip()
        app.save_settings()

        # Push emergency number to cloud API automatically
        threading.Thread(target=self._push_to_cloud,
                         args=(app.base_url, app.emergency_contact),
                         daemon=True).start()

        self._status.text  = '✅  Saving...'
        self._status.color = C['green']
        Clock.schedule_once(lambda dt: setattr(self.manager,
                                               'current', 'home'), 1.0)

    def _push_to_cloud(self, base_url, emergency_to):
        """Push emergency contact number to cloud API."""
        try:
            import urllib.request, json as _j, ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode    = ssl.CERT_NONE
            data = _j.dumps({'emergency_to': emergency_to}).encode()
            req  = urllib.request.Request(
                f"{base_url}/settings",
                data=data, method='POST')
            req.add_header('Content-Type', 'application/json')
            urllib.request.urlopen(req, timeout=8, context=ctx)
            print(f"Emergency contact pushed to cloud: {emergency_to}")
        except Exception as e:
            print(f"Could not push to cloud: {e}")

    def _test(self, *_):
        ip  = self._ip.text.strip()
        url = (f"https://{ip}/ping" if self._sw.active
               else f"http://{ip}:{self._port.text.strip()}/ping")
        self._status.text  = '⏳  Testing...'
        self._status.color = C['orange']

        def _do():
            try:
                import urllib.request, json as _j, ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                r = urllib.request.urlopen(url, timeout=8, context=ctx)
                d = _j.loads(r.read().decode())
                msg = (f"✅  {d.get('model','?')}  "
                       f"{d.get('accuracy',0)*100:.1f}%  online")
                Clock.schedule_once(
                    lambda dt: self._set_st(msg, C['green']))
            except Exception as e:
                Clock.schedule_once(
                    lambda dt: self._set_st(f"❌  {str(e)[:45]}", C['red']))
        threading.Thread(target=_do, daemon=True).start()

    def _set_st(self, t, c):
        self._status.text  = t
        self._status.color = c

    def on_enter(self):
        """Load saved settings when screen opens."""
        app = App.get_running_app()
        if app:
            self._emg.text = app.emergency_contact or ''
            ip = app.base_url.replace('https://','').replace('http://','').split(':')[0]
            self._ip.text  = ip


# ── History Screen ────────────────────────────────────────────────────────────
class HistoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(name='history', **kw)
        root = BoxLayout(orientation='vertical',
                         padding=[dp(16), dp(12), dp(16), dp(12)],
                         spacing=dp(12))
        with root.canvas.before:
            Color(*C['bg'])
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda w, v: setattr(self._bg, 'pos', v),
                  size=lambda w, v: setattr(self._bg, 'size', v))

        # Header
        hdr = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(10))
        hdr.add_widget(pill_btn('←', bg=C['card2'], r=10,
                                size_hint=(None, None), size=(dp(42), dp(42)),
                                cb=lambda _: setattr(self.manager,
                                                     'current', 'home')))
        hdr.add_widget(txt('[b]Fall History[/b]', size=20,
                           color=C['white'], halign='left'))
        hdr.add_widget(pill_btn('🔄', bg=C['card2'], r=10,
                                size_hint=(None, None), size=(dp(42), dp(42)),
                                cb=self._load))
        root.add_widget(hdr)

        # Summary card
        self._summary = GlassCard(bg=C['card'], radius=14,
                                  orientation='vertical',
                                  size_hint_y=None, height=dp(70),
                                  padding=dp(14), spacing=dp(4))
        self._sum_lbl = txt('Loading fall history...', size=13,
                            color=C['grey'])
        self._summary.add_widget(self._sum_lbl)
        root.add_widget(self._summary)

        scroll = ScrollView()
        self._list = BoxLayout(orientation='vertical', spacing=dp(8),
                               size_hint_y=None, padding=[0, dp(4)])
        self._list.bind(minimum_height=self._list.setter('height'))
        scroll.add_widget(self._list)
        root.add_widget(scroll)

        self.add_widget(root)

    def on_enter(self):
        self._load()

    def _load(self, *_):
        def _do():
            try:
                import urllib.request, json as _j, ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                r = urllib.request.urlopen(
                    f"{App.get_running_app().base_url}/history",
                    timeout=6, context=ctx)
                Clock.schedule_once(
                    lambda dt: self._show(_j.loads(r.read().decode()).get('falls', [])))
            except Exception as e:
                Clock.schedule_once(
                    lambda dt: self._show_err(str(e)))
        threading.Thread(target=_do, daemon=True).start()

    def _show(self, falls):
        self._list.clear_widgets()
        n = len(falls)
        self._sum_lbl.text = (
            f"[b]{n}[/b] fall event{'s' if n != 1 else ''} recorded"
            if n else 'No fall events recorded yet')
        self._sum_lbl.color = C['red'] if n else C['green']

        if not falls:
            empty = GlassCard(bg=C['card2'], radius=12,
                              size_hint_y=None, height=dp(80),
                              padding=dp(16))
            empty.add_widget(txt('✅  All clear — no falls detected',
                                 size=13, color=C['green']))
            self._list.add_widget(empty)
            return

        for i, ev in enumerate(reversed(falls)):
            card = GlassCard(bg=C['dark_red'], radius=14,
                             orientation='vertical',
                             size_hint_y=None, height=dp(72),
                             padding=[dp(14), dp(10)], spacing=dp(4))

            top = BoxLayout(size_hint_y=None, height=dp(28))
            top.add_widget(txt('🚨  FALL DETECTED', size=14, bold=True,
                               color=C['red'], halign='left'))
            p = ev.get('probability', 0)
            top.add_widget(txt(f"{p*100:.0f}%", size=14, bold=True,
                               color=C['red2'], halign='right'))
            card.add_widget(top)

            t = ev.get('time', '')
            card.add_widget(txt(f"📅  {t[:10]}   🕐  {t[11:19]}",
                                size=11, color=C['grey'], halign='left',
                                size_hint_y=None, height=dp(20)))
            self._list.add_widget(card)

    def _show_err(self, msg):
        self._list.clear_widgets()
        err = GlassCard(bg=C['card2'], radius=12,
                        size_hint_y=None, height=dp(60), padding=dp(14))
        err.add_widget(txt(f'❌  {msg[:50]}', size=12, color=C['red']))
        self._list.add_widget(err)


# ── App ───────────────────────────────────────────────────────────────────────
class FallGuardApp(App):
    base_url          = CLOUD_URL
    emergency_contact = ''   # phone number for SMS alerts

    def build(self):
        self.title = 'Fall Guard'
        # Load saved settings
        self._load_settings()
        sm = ScreenManager(transition=FadeTransition(duration=0.15))
        sm.add_widget(SplashScreen())
        sm.add_widget(HomeScreen())
        sm.add_widget(SettingsScreen())
        sm.add_widget(HistoryScreen())
        return sm

    def _load_settings(self):
        """Load saved settings from file."""
        try:
            settings_file = os.path.join(
                os.path.expanduser('~'), '.fallguard_settings.json')
            if os.path.exists(settings_file):
                with open(settings_file) as f:
                    data = json.load(f)
                saved_url = data.get('base_url', CLOUD_URL)
                # Validate — if saved URL is empty or localhost, use cloud
                if saved_url and 'localhost' not in saved_url and '127.0.0.1' not in saved_url:
                    self.base_url = saved_url
                else:
                    self.base_url = CLOUD_URL
                self.emergency_contact = data.get('emergency_contact', '')
        except Exception:
            self.base_url = CLOUD_URL

    def save_settings(self):
        """Save settings to file."""
        try:
            settings_file = os.path.join(
                os.path.expanduser('~'), '.fallguard_settings.json')
            with open(settings_file, 'w') as f:
                json.dump({
                    'base_url'          : self.base_url,
                    'emergency_contact' : self.emergency_contact
                }, f)
        except Exception:
            pass


if __name__ == '__main__':
    FallGuardApp().run()
