import traceback

###########################################################################################################
#
#
# 	Reporter Plugin
#
# 	Read the docs:
# 	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################
import objc
from AppKit import NSColor, NSGraphicsContext
from GlyphsApp import Glyphs
from GlyphsApp.plugins import ReporterPlugin

plugin_id = "ShowGlobalGlyph"
FILL_CLOSED_PATHS_KEY = f"{plugin_id}FillClosedPaths"
FILL_OPEN_PATHS_KEY = f"{plugin_id}FillOpenPaths"
CLOSED_PATHS_COLOR_KEY = f"{plugin_id}ClosedPathsColor"
OPEN_PATHS_COLOR_KEY = f"{plugin_id}OpenPathsColor"
CLOSED_PATHS_FILL_COLOR_KEY = f"{plugin_id}ClosedPathsFillColor"
OPEN_PATHS_FILL_COLOR_KEY = f"{plugin_id}OpenPathsFillColor"
GLOBAL_GLYPH_NAME_KEY = f"{plugin_id}GlyphName"


def nsc(r, g, b, a) -> NSColor:
    return NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)


class classGlobalGlyph(ReporterPlugin):
    @objc.python_method
    def settings(self):
        self.menuName = Glyphs.localize(
            {
                "en": "Global Glyph",
                "de": "Globale Glyphe",
                "es": "glifo global",
                "fr": "glyphe global",
            }
        )

        # Upgrade older color values
        for key, color in (
            (CLOSED_PATHS_FILL_COLOR_KEY, (1.0, 0.7, 1.2, 0.1)),
            (CLOSED_PATHS_COLOR_KEY, (1.0, 0.7, 0.2, 1.0)),
            (OPEN_PATHS_FILL_COLOR_KEY, (0.0, 0.0, 1.0, 0.1)),
            (OPEN_PATHS_COLOR_KEY, (0.0, 0.0, 1.0, 0.9)),
        ):
            if Glyphs.defaults[key] == color or Glyphs.defaults[key] is None:
                Glyphs.colorDefaults[key] = nsc(*color)

        Glyphs.registerDefaults(
            {
                GLOBAL_GLYPH_NAME_KEY: "_global",
                FILL_CLOSED_PATHS_KEY: True,
                FILL_OPEN_PATHS_KEY: True,
                # CLOSED_PATHS_FILL_COLOR_KEY: (1.0, 0.7, 1.2, 0.1),
                # CLOSED_PATHS_COLOR_KEY: (1.0, 0.7, 0.2, 1.0),
                # OPEN_PATHS_FILL_COLOR_KEY: (0.0, 0.0, 1.0, 0.1),
                # OPEN_PATHS_COLOR_KEY: (0.0, 0.0, 1.0, 0.9),
            }
        )

        if Glyphs.versionNumber < 4.0:
            return

        # Glyphs 4: Make settings editable from the Advanced Preferences dialog
        GSAdvancedPreferences = objc.lookUpClass("GSAdvancedPreferences")
        GSAdvancedPreferences.sharedAdvancedPreferences().registerEntries_forCategory_(
            [
                {
                    "title": "Global glyph name",
                    "key": GLOBAL_GLYPH_NAME_KEY,
                    "type": "string",
                },
                {
                    "title": "Closed paths color",
                    "key": CLOSED_PATHS_COLOR_KEY,
                    "type": "color",
                },
                {
                    "title": "Fill closed paths",
                    "key": FILL_CLOSED_PATHS_KEY,
                    "type": "bool",
                },
                {
                    "title": "Closed paths fill color",
                    "key": CLOSED_PATHS_FILL_COLOR_KEY,
                    "type": "color",
                },
                {
                    "title": "Open paths color",
                    "key": OPEN_PATHS_COLOR_KEY,
                    "type": "color",
                },
                {
                    "title": "Fill open paths",
                    "key": FILL_OPEN_PATHS_KEY,
                    "type": "bool",
                },
                {
                    "title": "Open paths fill color",
                    "key": OPEN_PATHS_FILL_COLOR_KEY,
                    "type": "color",
                },
            ],
            "Global Glyph",
        )

    @objc.python_method
    def drawGlobalGlyph(self, layer):
        glyph = layer.parent
        globalGlyphName = Glyphs.defaults[GLOBAL_GLYPH_NAME_KEY]
        if glyph.name == globalGlyphName:
            return

        Font = glyph.parent
        globalGlyph = Font.glyphForName_(globalGlyphName)
        if globalGlyph is None:
            return

        thisMasterID = layer.master.id
        globalLayer = globalGlyph.layers[thisMasterID]

        NSGraphicsContext.saveGraphicsState()
        scaledLineWidth = 1 / self.getScale()

        # Draw closed paths and components
        globalBezierPath = globalLayer.completeBezierPath
        if globalBezierPath:
            globalBezierPath.setLineWidth_(scaledLineWidth)
            if Glyphs.defaults[FILL_CLOSED_PATHS_KEY]:
                Glyphs.colorDefaults[CLOSED_PATHS_FILL_COLOR_KEY].set()
                globalBezierPath.fill()
            Glyphs.colorDefaults[CLOSED_PATHS_COLOR_KEY].set()
            globalBezierPath.stroke()

        # Draw open paths
        globalBezierPath = globalLayer.openBezierPath
        if globalBezierPath:
            globalBezierPath.setLineWidth_(scaledLineWidth)
            if Glyphs.defaults[FILL_OPEN_PATHS_KEY]:
                Glyphs.colorDefaults[OPEN_PATHS_FILL_COLOR_KEY].set()
                globalBezierPath.fill()
            Glyphs.colorDefaults[OPEN_PATHS_COLOR_KEY].set()
            globalBezierPath.stroke()

        NSGraphicsContext.restoreGraphicsState()

    @objc.python_method
    def background(self, layer):
        try:
            self.drawGlobalGlyph(layer)
        except:  # noqa: E722
            self.logError(traceback.format_exc())

    @objc.python_method
    def inactiveLayerBackground(self, layer):
        try:
            self.drawGlobalGlyph(layer)
        except:  # noqa: E722
            self.logError(traceback.format_exc())

    @objc.python_method
    def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
        return True

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
