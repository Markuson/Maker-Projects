#!/usr/bin/env python3
"""
weather_ui.py - UI per display e-ink 2.13" V4
Layout dividit: Temperatures (esquerra) | Previsió (dreta)
"""

import sys
from PIL import Image, ImageDraw, ImageFont
import math

# Afegir path del display wrapper
sys.path.append('/root/projects/dietpink/software/eink')
from dietpink_display import DietpinkDisplay


class WeatherUI:
    """UI per mostrar temperatures i previsió al display e-ink"""
    
    # Dimensions display 2.13" V4 (rotated 90°)
    WIDTH = 250
    HEIGHT = 122
    
    # Layout split vertical
    SPLIT_X = 125  # Meitat
    
    def __init__(self):
        """Inicialitzar UI"""
        self.display = DietpinkDisplay()
        
        # Fonts (sistema)
        try:
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            self.font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            print("⚠️  Font truetype no disponible, usant font per defecte")
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()
    
    def render(self, temp_interior, temp_exterior, forecast):
        """
        Renderitzar UI complet
        
        Args:
            temp_interior: Temperatura menjador (float o None)
            temp_exterior: Temperatura balcó (float o None)
            forecast: Dict amb dades de previsió YR
        """
        print(f"   [UI] render() cridat amb: IN={temp_interior}, OUT={temp_exterior}, forecast={forecast.get('symbol_code') if forecast else None}")

        # Crear imatge
        image = Image.new('1', (self.WIDTH, self.HEIGHT), 255)  # Blanc
        draw = ImageDraw.Draw(image)
        
        # Línia divisoria vertical
        draw.line([(self.SPLIT_X, 0), (self.SPLIT_X, self.HEIGHT)], fill=0, width=2)
        
        # Secció esquerra: Temperatures
        self._draw_temperatures(draw, temp_interior, temp_exterior)
        
        # Secció dreta: Previsió
        self._draw_forecast(draw, forecast)
       
        # Rotar 180 graus
        image = image.rotate(180)

        # Mostrar al display
        self.display.show_image(image)
    
    def _draw_temperatures(self, draw, temp_interior, temp_exterior):
        """Dibuixar secció de temperatures (esquerra)"""
        
        # Zona interior (casa)
        house_x = 5
        house_y = 2
        house_w = 110
        house_h = 75
        
        # Dibuixar "casa" (rectangle amb "sostre")
        # Sostre (triangle)
        roof_points = [
            (house_x, house_y + 12),
            (house_x + house_w // 2, house_y),
            (house_x + house_w, house_y + 12)
        ]
        draw.polygon(roof_points, outline=0, fill=255)
        
        # Parets
        draw.rectangle(
            [house_x, house_y + 12, house_x + house_w, house_y + house_h],
            outline=0,
            width=2
        )
        
        # Temperatura interior dins casa - CENTRADA VERTICALMENT I HORITZONTALMENT
        if temp_interior is not None:
            temp_text = f"{temp_interior:.0f}°C"
            
            # Calcular mida del text
            bbox = draw.textbbox((0, 0), temp_text, font=self.font_large)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            
            # Centrar dins l'àrea de la casa (exclou sostre)
            house_inner_h = house_h - 12  # Altura útil sense sostre
            text_x = house_x + (house_w - text_w) // 2
            text_y = house_y + 12 + (house_inner_h - text_h) // 2
            
            draw.text((text_x, text_y), temp_text, font=self.font_large, fill=0)
        else:
            draw.text((house_x + 25, house_y + 28), "---", font=self.font_large, fill=0)
        
        # Temperatura exterior (fora de casa) - més avall
        ext_y = house_y + house_h + 5
        
        if temp_exterior is not None:
            temp_text = f"{temp_exterior:.0f}°C"
            
            # Centrar horitzontalment a la secció esquerra
            bbox = draw.textbbox((0, 0), temp_text, font=self.font_large)
            text_w = bbox[2] - bbox[0]
            text_x = (self.SPLIT_X - text_w) // 2
            
            draw.text((text_x, ext_y), temp_text, font=self.font_large, fill=0)
            
        else:
            draw.text((40, ext_y), "---", font=self.font_large, fill=0)
    
    def _draw_forecast(self, draw, forecast):
        """Dibuixar secció de previsió (dreta)"""
        
        start_x = self.SPLIT_X + 8
        section_width = self.WIDTH - self.SPLIT_X - 16  # Amplada útil
        
        # ========================================
        # PART 1: Icona meteorològica (dalt)
        # ========================================
        
        # Calcular posició centre de la icona
        icon_x = self.SPLIT_X + (section_width // 2) + 8
        icon_y = 32  # Centrat verticalment a la part superior
        icon_size = 38  # Mida de la icona
        
        # Dibuixar icona
        self._draw_weather_icon(draw, icon_x, icon_y, icon_size, 
                               forecast.get('symbol_code', 'unknown'))
        
        # ========================================
        # PART 2: Dades al bottom (espaiament uniforme)
        # ========================================
        
        # Definir dades
        temp_max = forecast.get('temperature_max', 0)
        temp_min = forecast.get('temperature_min', 0)
        precip = forecast.get('precipitation', 0)
        wind_speed = forecast.get('wind_speed', 0)
        wind_dir = forecast.get('wind_direction', 0)
        wind_kmh = wind_speed * 3.6
        
        data_lines = [
            f"Max: {temp_max:.0f}C",
            f"Min: {temp_min:.0f}C",
            f"Rain: {precip:.1f}mm",
            f"Wind: {wind_kmh:.0f}km/h"
        ]
        
        # Calcular espaiament uniforme
        data_height_total = 52  # Altura total per les 4 línies
        data_y_start = self.HEIGHT - data_height_total - 2  # 5px marge inferior
        
        num_lines = len(data_lines)
        spacing = data_height_total // num_lines  # Espai entre línies
        
        # Dibuixar cada línia amb espaiament uniforme
        for i, line in enumerate(data_lines):
            y_pos = data_y_start + (i * spacing)
            draw.text((start_x, y_pos), line, font=self.font_small, fill=0)
        
        # Fletxa de vent al costat de l'última línia
        arrow_x = start_x + 95
        arrow_y = data_y_start + ((num_lines - 1) * spacing) + 6
        self._draw_wind_arrow(draw, arrow_x, arrow_y, wind_dir)

    def _get_symbol_text(self, symbol_code):
        """
        Convertir symbol_code de YR a icona ASCII art visual
        """
        # Icones ASCII art de 3 línies
        symbol_map = {
            'clearsky': ['  \\   |   /', '   -- O --', '  /   |   \\'],
            'fair': ['  \\   |   /', '   -- O --', '  /   |   \\'],
            'partlycloudy': ['   ___', '  (   )', ' (_____)'],
            'cloudy': ['  _____', ' (     )', '(_______)'],
            'rain': ['  ___', ' (   )', '  | | |'],
            'lightrain': ['  ___', ' (   )', '  : : :'],
            'heavyrain': ['  ___', ' (   )', ' || || ||'],
            'snow': ['  ___', ' (   )', '  * * *'],
            'sleet': ['  ___', ' (   )', ' *:|:*'],
            'fog': ['  -----', ' ------', '  -----'],
        }
        
        # Buscar match parcial
        for key, icon_lines in symbol_map.items():
            if key in symbol_code:
                return icon_lines
        
        # Default: interrogant
        return ['  ???', '  ???', '  ???']

    def _draw_wind_arrow(self, draw, x, y, direction_degrees):
        """
        Dibuixar triangle indicant direcció del vent
        
        Args:
            x, y: Punt base del triangle
            direction_degrees: Direcció en graus (0=Nord, 90=Est, etc.)
        """
        import math
        
        # Convertir a radians (ajustar perquè 0° = Nord)
        angle = math.radians(direction_degrees - 90)
        
        # Mida del triangle
        height = 8  # Altura del triangle
        base = 6    # Amplada de la base
        
        # Calcular els 3 punts del triangle
        # Punt superior (punta del triangle, apunta en la direcció)
        tip_x = x + height * math.cos(angle)
        tip_y = y + height * math.sin(angle)
        
        # Angle perpendicular per la base
        perp_angle = angle + math.radians(90)
        
        # Punt esquerre de la base
        left_x = x + (base / 2) * math.cos(perp_angle)
        left_y = y + (base / 2) * math.sin(perp_angle)
        
        # Punt dret de la base
        right_x = x - (base / 2) * math.cos(perp_angle)
        right_y = y - (base / 2) * math.sin(perp_angle)
        
        # Dibuixar triangle ple (negre)
        points = [
            (tip_x, tip_y),    # Punta
            (left_x, left_y),  # Base esquerra
            (right_x, right_y) # Base dreta
        ]
        
        draw.polygon(points, fill=0, outline=0)   

    def _draw_weather_icon(self, draw, x, y, size, symbol_code):
        """
        Dibuixar icona meteorològica amb formes geomètriques
        
        Args:
            draw: ImageDraw object
            x, y: Posició centre de la icona
            size: Mida de la icona (radi base)
            symbol_code: Codi YR (clearsky, cloudy, rain, etc.)
        """
        # Determinar tipus d'icona
        if 'clearsky' in symbol_code or 'fair' in symbol_code:
            self._draw_sun_icon(draw, x, y, size)
        
        elif 'partlycloudy' in symbol_code:
            self._draw_partial_cloud_icon(draw, x, y, size)
        
        elif 'cloudy' in symbol_code:
            self._draw_cloud_icon(draw, x, y, size)
        
        elif 'rain' in symbol_code or 'shower' in symbol_code:
            self._draw_rain_icon(draw, x, y, size, symbol_code)
        
        elif 'snow' in symbol_code:
            self._draw_snow_icon(draw, x, y, size)
        
        elif 'sleet' in symbol_code:
            self._draw_sleet_icon(draw, x, y, size)
        
        elif 'fog' in symbol_code:
            self._draw_fog_icon(draw, x, y, size)
        
        else:
            # Unknown: dibuixar interrogant
            draw.text((x - 5, y - 8), "?", font=self.font_large, fill=0)
    
    def _draw_sun_icon(self, draw, cx, cy, size):
        """Dibuixar sol"""
        r = size // 2
        
        # Cercle central
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0, outline=0)
        
        # Raigs (8 línies)
        ray_len = size // 3
        import math
        for i in range(8):
            angle = math.radians(i * 45)
            x1 = cx + (r + 2) * math.cos(angle)
            y1 = cy + (r + 2) * math.sin(angle)
            x2 = cx + (r + 2 + ray_len) * math.cos(angle)
            y2 = cy + (r + 2 + ray_len) * math.sin(angle)
            draw.line([(x1, y1), (x2, y2)], fill=0, width=1)
    
    def _draw_cloud_icon(self, draw, cx, cy, size):
        """Dibuixar núvol"""
        # Núvol = 3 cercles sobreposats
        r1 = size // 3
        r2 = size // 2
        r3 = size // 3
        
        # Cercle esquerre
        draw.ellipse([cx - size//2 - r1, cy - r1//2, cx - size//2 + r1, cy + r1//2 + r1], 
                     outline=0, fill=255, width=2)
        
        # Cercle central (més gran)
        draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], 
                     outline=0, fill=255, width=2)
        
        # Cercle dret
        draw.ellipse([cx + size//2 - r3, cy - r3//2, cx + size//2 + r3, cy + r3//2 + r3], 
                     outline=0, fill=255, width=2)
        
        # Base del núvol (línia)
        draw.line([(cx - size//2, cy + r1), (cx + size//2, cy + r1)], fill=0, width=2)
    
    def _draw_partial_cloud_icon(self, draw, cx, cy, size):
        """Dibuixar sol parcial amb núvol"""
        # Sol petit a dalt esquerra
        sun_x = cx - size // 3
        sun_y = cy - size // 3
        sun_r = size // 4
        draw.ellipse([sun_x - sun_r, sun_y - sun_r, 
                     sun_x + sun_r, sun_y + sun_r], fill=0)
        
        # Raigs curts
        import math
        for i in [0, 1, 7]:  # Només 3 raigs visibles
            angle = math.radians(i * 45)
            x1 = sun_x + sun_r * math.cos(angle)
            y1 = sun_y + sun_r * math.sin(angle)
            x2 = sun_x + (sun_r + 4) * math.cos(angle)
            y2 = sun_y + (sun_r + 4) * math.sin(angle)
            draw.line([(x1, y1), (x2, y2)], fill=0, width=1)
        
        # Núvol davant
        cloud_y = cy + size // 6
        self._draw_cloud_icon(draw, cx + size//6, cloud_y, size * 2 // 3)
    
    def _draw_rain_icon(self, draw, cx, cy, size, symbol_code):
        """Dibuixar núvol amb pluja"""
        # Núvol a dalt
        self._draw_cloud_icon(draw, cx, cy - size//4, size)
        
        # Gotes de pluja
        rain_y = cy + size // 2
        
        if 'heavy' in symbol_code:
            # Pluja forta (més línies)
            for i in range(5):
                x = cx - size//2 + i * (size // 4)
                draw.line([(x, rain_y), (x, rain_y + size//3)], fill=0, width=2)
        else:
            # Pluja normal
            for i in range(3):
                x = cx - size//3 + i * (size // 3)
                draw.line([(x, rain_y), (x, rain_y + size//4)], fill=0, width=1)
    
    def _draw_snow_icon(self, draw, cx, cy, size):
        """Dibuixar núvol amb neu"""
        # Núvol
        self._draw_cloud_icon(draw, cx, cy - size//4, size)
        
        # Flocs de neu (asteriscs)
        snow_y = cy + size // 2
        snow_size = 3
        
        for i in range(3):
            x = cx - size//3 + i * (size // 3)
            # Dibuixar X
            draw.line([(x - snow_size, snow_y - snow_size), 
                      (x + snow_size, snow_y + snow_size)], fill=0, width=1)
            draw.line([(x - snow_size, snow_y + snow_size), 
                      (x + snow_size, snow_y - snow_size)], fill=0, width=1)
            # Creu vertical/horitzontal
            draw.line([(x, snow_y - snow_size), (x, snow_y + snow_size)], fill=0, width=1)
            draw.line([(x - snow_size, snow_y), (x + snow_size, snow_y)], fill=0, width=1)
    
    def _draw_sleet_icon(self, draw, cx, cy, size):
        """Dibuixar núvol amb aiguaneu"""
        # Núvol
        self._draw_cloud_icon(draw, cx, cy - size//4, size)
        
        # Mix de pluja i neu
        rain_y = cy + size // 2
        for i in range(3):
            x = cx - size//3 + i * (size // 3)
            if i % 2 == 0:
                # Gota
                draw.line([(x, rain_y), (x, rain_y + size//4)], fill=0, width=1)
            else:
                # Floc
                draw.line([(x - 2, rain_y), (x + 2, rain_y + 4)], fill=0, width=1)
                draw.line([(x - 2, rain_y + 4), (x + 2, rain_y)], fill=0, width=1)
    
    def _draw_fog_icon(self, draw, cx, cy, size):
        """Dibuixar boira (línies horitzontals)"""
        for i in range(4):
            y = cy - size//3 + i * (size // 5)
            x1 = cx - size//2
            x2 = cx + size//2
            # Línies de diferents longituds
            offset = (i % 2) * (size // 6)
            draw.line([(x1 + offset, y), (x2 - offset, y)], fill=0, width=1)
    
    def clear(self):
        """Netejar display"""
        self.display.clear()


# Test del mòdul
if __name__ == "__main__":
    import time
    
    print("🖼️  Test weather_ui.py")
    print("")
    
    # Crear UI
    ui = WeatherUI()
    
    # Dades de test
    temp_interior = 21.5
    temp_exterior = 8.2
    
    forecast_test = {
        'symbol_code': 'partlycloudy_day',
        'precipitation': 2.3,
        'temperature_max': 15,
        'temperature_min': 8,
        'wind_speed': 3.3,  # m/s
        'wind_direction': 90,  # Est
        'success': True
    }
    
    print("📊 Renderitzant UI de test...")
    ui.render(temp_interior, temp_exterior, forecast_test)
    
    print("✅ UI mostrada al display!")
    print("   (Espera 5 segons...)")
    time.sleep(5)
    
    print("🧹 Netejant display...")
    ui.clear()
    
    print("✅ Test completat!")
