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
from AppKit import NSColor
from GlyphsApp import Glyphs
from GlyphsApp.plugins import ReporterPlugin

plugin_id = "ShowGlobalGlyph"
FILL_CLOSED_PATHS_KEY = f"{plugin_id}FillClosedPaths"
FILL_OPEN_PATHS_KEY = f"{plugin_id}FillOpenPaths"
CLOSED_PATHS_COLOR_KEY = f"{plugin_id}ClosedPathsColor"
OPEN_PATHS_COLOR_KEY = f"{plugin_id}OpenPathsColor"
CLOSED_PATHS_FILL_COLOR_KEY = f"{plugin_id}ClosedPathsFillColor"
OPEN_PATHS_FILL_COLOR_KEY = f"{plugin_id}OpenPathsFillColor"


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

        self.globalGlyphName = "_global"
        self.fillOpenPaths = Glyphs.defaults.get(FILL_OPEN_PATHS_KEY, True)
        self.fillClosedPaths = Glyphs.defaults.get(FILL_CLOSED_PATHS_KEY, True)
        self.openPathsColor = Glyphs.defaults.get(
            OPEN_PATHS_COLOR_KEY, (0.0, 0.0, 1.0, 0.9)
        )
        self.closedPathsColor = Glyphs.defaults.get(
            CLOSED_PATHS_COLOR_KEY, (1.0, 0.7, 0.2, 1.0)
        )
        self.openPathsFillColor = Glyphs.defaults.get(
            OPEN_PATHS_FILL_COLOR_KEY, (0.0, 0.0, 1.0, 0.1)
        )
        self.closedPathsFillColor = Glyphs.defaults.get(
            CLOSED_PATHS_FILL_COLOR_KEY, (1.0, 0.7, 0.2, 0.1)
        )

    @objc.python_method
    def drawGlobalGlyph(self, layer):
        glyph = layer.parent
        if glyph.name == self.globalGlyphName:
            return

        Font = glyph.parent
        globalGlyph = Font.glyphForName_(self.globalGlyphName)
        if globalGlyph is None:
            return

        thisMasterID = layer.master.id
        globalLayer = globalGlyph.layers[thisMasterID]

        # draw path AND components for strokes and form:
        globalBezierPath = globalLayer.completeBezierPath
        if globalBezierPath:
            if self.fillClosedPaths:
                NSColor.colorWithCalibratedRed_green_blue_alpha_(
                    *self.closedPathsFillColor
                ).set()
                globalBezierPath.fill()
            NSColor.colorWithCalibratedRed_green_blue_alpha_(
                *self.closedPathsColor
            ).set()
            globalBezierPath.stroke()

        # draw path for open forms
        globalBezierPath = globalLayer.openBezierPath
        if globalBezierPath:
            if self.fillOpenPaths:
                NSColor.colorWithCalibratedRed_green_blue_alpha_(
                    *self.openPathsFillColor
                ).set()
                globalBezierPath.fill()
            NSColor.colorWithCalibratedRed_green_blue_alpha_(*self.openPathsColor).set()
            globalBezierPath.stroke()

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
