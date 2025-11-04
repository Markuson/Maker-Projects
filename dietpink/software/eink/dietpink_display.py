"""
DietpinkDisplay - Wrapper personalitzat per e-ink 2.13" V4
Simplifica l'ús del display per al projecte dietpink
"""

import sys
import os
import time
from PIL import Image, ImageDraw, ImageFont

# Path al driver WaveShare
LIBDIR = '/root/projects/dietpink/software/eink/drivers/e-Paper/RaspberryPi_JetsonNano/python/lib'
if os.path.exists(LIBDIR):
    sys.path.append(LIBDIR)

from waveshare_epd import epd2in13_V4

class DietpinkDisplay:
    """
    Wrapper per WaveShare e-ink 2.13" V4
    Facilita operacions comunes
    """

    # Dimensions del display (landscape)
    WIDTH = 122
    HEIGHT = 250

    # Colors (mode 1-bit)
    WHITE = 255
    BLACK = 0

    def __init__(self):
        """Inicialitzar display"""
        print("🎨 Inicialitzant DietpinkDisplay...")
        self.epd = epd2in13_V4.EPD()
        self.epd.init()

	# Clear físic del display per eliminar ghosting
    	print("🧹 Netejant display físic...")
    	self.epd.Clear(0xFF)  # 0xFF = blanc

	# Crear canvas (imatge base)
        self.image = Image.new('1', (self.HEIGHT, self.WIDTH), self.WHITE)
        self.draw = ImageDraw.Draw(self.image)
        
        # Carregar fonts
        self._load_fonts()
        
        print(f"✅ Display llest ({self.HEIGHT}x{self.WIDTH})")
    
    def _load_fonts(self):
        """Carregar fonts del sistema"""
        font_path = '/usr/share/fonts/truetype/dejavu/'
        try:
            self.font_tiny = ImageFont.truetype(f'{font_path}DejaVuSans.ttf', 10)
            self.font_small = ImageFont.truetype(f'{font_path}DejaVuSans.ttf', 12)
            self.font_medium = ImageFont.truetype(f'{font_path}DejaVuSans.ttf', 16)
            self.font_large = ImageFont.truetype(f'{font_path}DejaVuSans-Bold.ttf', 24)
            self.font_huge = ImageFont.truetype(f'{font_path}DejaVuSans-Bold.ttf', 36)
            print("✅ Fonts carregades")
        except Exception as e:
            print(f"⚠️  Error carregant fonts: {e}")
            self.font_tiny = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
            self.font_huge = ImageFont.load_default()
    
    def clear(self, color=None):
        """
        Netejar canvas (no actualitza display)
        
        Args:
            color: WHITE o BLACK (None = WHITE)
        """
        if color is None:
            color = self.WHITE
        self.image = Image.new('1', (self.HEIGHT, self.WIDTH), color)
        self.draw = ImageDraw.Draw(self.image)
    
    def text(self, text, x, y, size='medium', color=None, align='left'):
        """
        Dibuixar text al canvas
        
        Args:
            text: Text a mostrar
            x, y: Posició
            size: 'tiny', 'small', 'medium', 'large', 'huge'
            color: BLACK o WHITE (None = BLACK)
            align: 'left', 'center', 'right'
        """
        if color is None:
            color = self.BLACK
            
        fonts = {
            'tiny': self.font_tiny,
            'small': self.font_small,
            'medium': self.font_medium,
            'large': self.font_large,
            'huge': self.font_huge
        }
        font = fonts.get(size, self.font_medium)
        
        # Ajustar posició segons alignment
        if align == 'center':
            bbox = self.draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = x - text_width // 2
        elif align == 'right':
            bbox = self.draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = x - text_width
        
        self.draw.text((x, y), text, font=font, fill=color)
    
    def rectangle(self, x, y, width, height, fill=None, outline=None, width_line=1):
        """
        Dibuixar rectangle
        
        Args:
            x, y: Posició top-left
            width, height: Dimensions
            fill: Color farcit (None = transparent)
            outline: Color contorn (None = sense contorn)
            width_line: Gruix línia
        """
        if outline is None and fill is None:
            outline = self.BLACK
            
        self.draw.rectangle(
            (x, y, x + width, y + height),
            fill=fill,
            outline=outline,
            width=width_line
        )
    
    def line(self, x1, y1, x2, y2, color=None, width=1):
        """Dibuixar línia"""
        if color is None:
            color = self.BLACK
        self.draw.line((x1, y1, x2, y2), fill=color, width=width)
    
    def circle(self, x, y, radius, fill=None, outline=None, width=1):
        """Dibuixar cercle (center x,y)"""
        if outline is None and fill is None:
            outline = self.BLACK
            
        bbox = (x - radius, y - radius, x + radius, y + radius)
        self.draw.ellipse(bbox, fill=fill, outline=outline, width=width)
    
    def progress_bar(self, x, y, width, height, percentage, 
                     bg_color=None, fill_color=None, border=True):
        """
        Dibuixar barra de progrés
        
        Args:
            x, y: Posició
            width, height: Dimensions
            percentage: 0-100
            bg_color: Color de fons
            fill_color: Color del farcit
            border: Mostrar vora?
        """
        if bg_color is None:
            bg_color = self.WHITE
        if fill_color is None:
            fill_color = self.BLACK
            
        # Fons
        self.rectangle(x, y, width, height, fill=bg_color, 
                      outline=self.BLACK if border else None)
        
        # Farcit segons percentatge
        fill_width = int((width - 4) * (percentage / 100))
        if fill_width > 0:
            self.rectangle(x + 2, y + 2, fill_width, height - 4, fill=fill_color)
    
    def image_from_file(self, path, x, y, width=None, height=None):
        """
        Carregar i dibuixar imatge des de fitxer
        
        Args:
            path: Path al fitxer imatge
            x, y: Posició
            width, height: Redimensionar (opcional)
        """
        try:
            img = Image.open(path)
            
            if width and height:
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convertir a 1-bit
            img = img.convert('1')
            
            # Pegar al canvas
            self.image.paste(img, (x, y))
        except Exception as e:
            print(f"⚠️  Error carregant imatge {path}: {e}")
    
    def refresh(self, partial=False):
        """
        Actualitzar display físic
        
        Args:
            partial: Usar partial refresh (més ràpid, menys ghosting)
        """
        if partial:
            self.epd.displayPartial(self.epd.getbuffer(self.image))
        else:
            self.epd.display(self.epd.getbuffer(self.image))
    
    def sleep(self):
        """Posar display en sleep mode (baix consum)"""
        self.epd.sleep()
    
    def clear_display(self):
        """Netejar display físic (blanc)"""
        self.epd.Clear(0xFF)
    
    def get_text_size(self, text, size='medium'):
        """
        Obtenir dimensions d'un text
        
        Returns:
            (width, height) en pixels
        """
        fonts = {
            'tiny': self.font_tiny,
            'small': self.font_small,
            'medium': self.font_medium,
            'large': self.font_large,
            'huge': self.font_huge
        }
        font = fonts.get(size, self.font_medium)
        bbox = self.draw.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])
    
    def __enter__(self):
        """Context manager support: with DietpinkDisplay() as display:"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto cleanup"""
        self.sleep()


# ============================================================================
# TEST DEL WRAPPER
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Test del DietpinkDisplay wrapper")
    print("=" * 50)
    
    try:
        with DietpinkDisplay() as display:
            # Test 1: Text bàsic
            print("\n📝 Test 1: Text en diferents mides")
            display.clear()
            display.text("dietpink", 125, 10, size='large', align='center')
            display.line(10, 35, 240, 35)
            display.text("Tiny text", 10, 45, size='tiny')
            display.text("Small text", 10, 60, size='small')
            display.text("Medium text", 10, 75, size='medium')
            display.refresh()
            time.sleep(3)
            
            # Test 2: Formes
            print("\n🔷 Test 2: Formes geomètriques")
            display.clear()
            display.rectangle(10, 10, 60, 40, outline=display.BLACK, width_line=2)
            display.rectangle(80, 10, 60, 40, fill=display.BLACK)
            display.circle(40, 70, 15, outline=display.BLACK, width=2)
            display.circle(110, 70, 15, fill=display.BLACK)
            display.line(10, 100, 150, 100, width=3)
            display.refresh()
            time.sleep(3)
            
            # Test 3: Progress bar
            print("\n📊 Test 3: Barra de progrés")
            display.clear()
            display.text("Progress bars:", 10, 10, size='small')
            display.progress_bar(10, 30, 200, 15, 25)
            display.text("25%", 220, 30, size='tiny')
            display.progress_bar(10, 55, 200, 15, 50)
            display.text("50%", 220, 55, size='tiny')
            display.progress_bar(10, 80, 200, 15, 75)
            display.text("75%", 220, 80, size='tiny')
            display.progress_bar(10, 105, 200, 15, 100)
            display.text("100%", 220, 105, size='tiny')
            display.refresh()
            time.sleep(3)
            
            # Test 4: Dashboard example
            print("\n📺 Test 4: Mini dashboard")
            display.clear()
            
            # Header
            display.rectangle(0, 0, 250, 30, fill=display.BLACK)
            display.text("dietpink", 125, 5, size='large', 
                        color=display.WHITE, align='center')
            
            # Content
            display.text(time.strftime('%Y-%m-%d'), 10, 40, size='small')
            display.text(time.strftime('%H:%M:%S'), 10, 60, size='huge')
            
            # Footer
            display.line(5, 105, 245, 105)
            display.text("2.13\" V4", 10, 110, size='tiny')
            display.text("Ready", 200, 110, size='tiny')
            
            display.refresh()
            time.sleep(3)
            
            print("\n✅ Tots els tests completats!")
            
    except KeyboardInterrupt:
        print("\n⚠️  Interromput per usuari")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✨ Test finalitzat")
    print("=" * 50)
