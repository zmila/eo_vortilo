import pytest
import sys
from pathlib import Path

# Add parent directory to path to import iloj module
sys.path.insert(0, str(Path(__file__).parent.parent))

from iloj.du_litera_silab_ilo import DuLiteraSilabiIlo, Silabo


class TestDuLiteraSilabiIlo:
    """Test cases for DuLiteraSilabiIlo.dividu_laŭ_avk method."""

    @pytest.fixture
    def ilo(self):
        """Create a DuLiteraSilabiIlo instance for testing."""
        return DuLiteraSilabiIlo()

    # Test cases from the specification examples
    def test_iu(self, ilo):
        """Test: iu → <xI-xU"""
        result = ilo.dividu_laŭ_avk("iu")
        assert ilo.skribu_avk(result) == "<xI-xU"

    def test_alta(self, ilo):
        """Test: alta → <xA-Ly-TA"""
        result = ilo.dividu_laŭ_avk("alta")
        assert ilo.skribu_avk(result) == "<xA-Ly-TA"

    def test_mem(self, ilo):
        """Test: mem → ME-My>"""
        result = ilo.dividu_laŭ_avk("mem")
        assert ilo.skribu_avk(result) == "ME-My>"

    def test_trans(self, ilo):
        """Test: trans → Ty-RA-Ny-Sy>"""
        result = ilo.dividu_laŭ_avk("trans")
        assert ilo.skribu_avk(result) == "Ty-RA-Ny-Sy>"

    def test_gemaljuneguletoj(self, ilo):
        """Test: gemaljuneguletoj → GE-MA-Ly-JU-NE-GU-LE-TO-Jy>"""
        result = ilo.dividu_laŭ_avk("gemaljuneguletoj")
        assert ilo.skribu_avk(result) == "GE-MA-Ly-JU-NE-GU-LE-TO-Jy>"

    def test_babiletemulegoj(self, ilo):
        """Test: babiletemulegoj → BA-BI-LE-TE-MU-LE-GO-Jy>"""
        result = ilo.dividu_laŭ_avk("babiletemulegoj")
        assert ilo.skribu_avk(result) == "BA-BI-LE-TE-MU-LE-GO-Jy>"

    # Edge case tests
    def test_empty_string(self, ilo):
        """Test: empty string returns empty string"""
        result = ilo.dividu_laŭ_avk("")
        assert ilo.skribu_avk(result) == ""

    def test_single_vowel(self, ilo):
        """Test: single vowel → <xA"""
        result = ilo.dividu_laŭ_avk("a")
        assert ilo.skribu_avk(result) == "<xA"

    def test_single_consonant(self, ilo):
        """Test: single consonant → By>"""
        result = ilo.dividu_laŭ_avk("b")
        assert ilo.skribu_avk(result) == "By>"

    def test_multiple_consonants_in_row(self, ilo):
        """Test: multiple consonants each get y if no vowel after"""
        result = ilo.dividu_laŭ_avk("ktp")
        assert ilo.skribu_avk(result) == "Ky-Ty-Py>"

    def test_uppercase_input(self, ilo):
        """Test: uppercase input is normalized to lowercase"""
        result = ilo.dividu_laŭ_avk("MEM")
        assert ilo.skribu_avk(result) == "ME-My>"

    def test_aero(self, ilo):
        """Test: aero → <xA-xE-RO"""
        result = ilo.dividu_laŭ_avk("aero")
        assert ilo.skribu_avk(result) == "<xA-xE-RO"

    # Test cases for SKIP_CHARS (apostrophe, underscore, dash)
    def test_skip_chars_avk(self, ilo):
        """Test: AVK mode skips apostrophe, underscore, and dash characters
        Input: radik-o'a_n (should be processed as radikoan)
        Expected: RA-DI-KO-xA-Ny> (same as if input was 'radikoan')
        """
        result_with_skip = ilo.dividu_laŭ_avk("radik-o'a_n")
        result_plain = ilo.dividu_laŭ_avk("radikoan")
        assert ilo.skribu_avk(result_with_skip) == ilo.skribu_avk(result_plain)
        assert ilo.skribu_avk(result_with_skip) == "RA-DI-KO-xA-Ny>"

    def test_skip_chars_pvk(self, ilo):
        """Test: PVK mode skips apostrophe, underscore, and dash characters
        Input: radik-o'a_n (should be processed as radikoan)
        Expected: <yR-AD-IK-Ox-AN (PVK format, where 'o' followed by vowel 'a' uses NUL_KO x)
        """
        result_with_skip = ilo.dividu_laŭ_pvk("radik-o'a_n")
        result_plain = ilo.dividu_laŭ_pvk("radikoan")
        assert ilo.skribu_pvk(result_with_skip) == ilo.skribu_pvk(result_plain)
        assert ilo.skribu_pvk(result_with_skip) == "<yR-AD-IK-Ox-AN"

    def test_pvk_iu(self, ilo):
        """Test: iu → Ix-Ux>"""
        result = ilo.dividu_laŭ_pvk("iu")
        assert ilo.skribu_pvk(result) == "Ix-Ux>"

    def test_pvk_alta(self, ilo):
        """Test: alta → AL-yT-Ax>"""
        result = ilo.dividu_laŭ_pvk("alta")
        assert ilo.skribu_pvk(result) == "AL-yT-Ax>"

    def test_pvk_mem(self, ilo):
        """Test: mem → <yM-EM"""
        result = ilo.dividu_laŭ_pvk("mem")
        assert ilo.skribu_pvk(result) == "<yM-EM"

    def test_pvk_trans(self, ilo):
        """Test: trans → <yT-yR-AN-ys"""
        result = ilo.dividu_laŭ_pvk("trans")
        assert ilo.skribu_pvk(result) == "<yT-yR-AN-yS"

    def test_pvk_gemaljuneguletoj(self, ilo):
        """Test: gemaljuneguletoj → <yG-EM-AL-yJ-UN-EG-UL-ET-OJ"""
        result = ilo.dividu_laŭ_pvk("gemaljuneguletoj")
        assert ilo.skribu_pvk(result) == "<yG-EM-AL-yJ-UN-EG-UL-ET-OJ"

    def test_pvk_babiletemulegoj(self, ilo):
        """Test: babiletemulegoj → <yB-AB-IL-ET-EM-UL-EG-OJ"""
        result = ilo.dividu_laŭ_pvk("babiletemulegoj")
        assert ilo.skribu_pvk(result) == "<yB-AB-IL-ET-EM-UL-EG-OJ"

    def test_pvk_aero(self, ilo):
        """Test: aero → Ax-ER-Ox>"""
        result = ilo.dividu_laŭ_pvk("aero")
        assert ilo.skribu_pvk(result) == "Ax-ER-Ox>"

    # Tests for skribu_silabon_avk (KV order)
    def test_skribu_silabon_avk_kv(self, ilo):
        """Test: AVK regular consonant-vowel syllable (KV)"""
        silabo = Silabo(k="m", v="a")
        assert ilo.skribu_silabon_avk(silabo) == "MA"

    def test_skribu_silabon_avk_xv(self, ilo):
        """Test: AVK syllable with NUL_KO (xV)"""
        silabo = Silabo(k="x", v="a")
        assert ilo.skribu_silabon_avk(silabo) == "xA"

    def test_skribu_silabon_avk_ky(self, ilo):
        """Test: AVK syllable with NUL_VO (Ky)"""
        silabo = Silabo(k="m", v="y")
        assert ilo.skribu_silabon_avk(silabo) == "My"

    def test_skribu_silabon_avk_xy(self, ilo):
        """Test: AVK syllable with both NUL_KO and NUL_VO (xy)"""
        silabo = Silabo(k="x", v="y")
        assert ilo.skribu_silabon_avk(silabo) == "xy"

    def test_skribu_silabon_avk_kom(self, ilo):
        """Test: AVK syllable with NUL_KO_KOM (<xV) - first vowel without consonant"""
        silabo = Silabo(k="<x", v="a")
        assert ilo.skribu_silabon_avk(silabo) == "<xA"

    def test_skribu_silabon_avk_fin(self, ilo):
        """Test: AVK syllable with NUL_VO_FIN (Ky>) - last consonant without vowel"""
        silabo = Silabo(k="s", v="y>")
        assert ilo.skribu_silabon_avk(silabo) == "Sy>"

    # Tests for skribu_silabon_pvk (VC order)
    def test_skribu_silabon_pvk_vc(self, ilo):
        """Test: PVK regular vowel-consonant syllable (VC)"""
        silabo = Silabo(k="m", v="a")
        assert ilo.skribu_silabon_pvk(silabo) == "AM"

    def test_skribu_silabon_pvk_vx(self, ilo):
        """Test: PVK syllable with NUL_KO (Vx)"""
        silabo = Silabo(k="x", v="a")
        assert ilo.skribu_silabon_pvk(silabo) == "Ax"

    def test_skribu_silabon_pvk_vy(self, ilo):
        """Test: PVK syllable with NUL_VO (Vy)"""
        silabo = Silabo(k="m", v="y")
        assert ilo.skribu_silabon_pvk(silabo) == "yM"

    def test_skribu_silabon_pvk_yx(self, ilo):
        """Test: PVK syllable with both NUL_VO and NUL_KO (yx)"""
        silabo = Silabo(k="x", v="y")
        assert ilo.skribu_silabon_pvk(silabo) == "yx"

    def test_skribu_silabon_pvk_fin(self, ilo):
        """Test: PVK syllable with NUL_KO_FIN (Vx>)"""
        silabo = Silabo(k="x>", v="a")
        assert ilo.skribu_silabon_pvk(silabo) == "Ax>"

    def test_skribu_silabon_pvk_kom(self, ilo):
        """Test: PVK syllable with NUL_VO_KOM (<yT)"""
        silabo = Silabo(k="t", v="<y")
        assert ilo.skribu_silabon_pvk(silabo) == "<yT"

    # Tests for skribu_avk
    def test_skribu_avk_empty(self, ilo):
        """Test: skribu_avk of empty word returns empty string"""
        vorto = []
        assert ilo.skribu_avk(vorto) == ""

    def test_skribu_avk_one_syllable(self, ilo):
        """Test: skribu_avk of single syllable"""
        vorto = [Silabo(k="b", v="a")]
        assert ilo.skribu_avk(vorto) == "BA"

    def test_skribu_avk_multiple_syllables(self, ilo):
        """Test: skribu_avk with multiple syllables joined by hyphen"""
        vorto = ilo.dividu_laŭ_avk("alta")
        assert ilo.skribu_avk(vorto) == "<xA-Ly-TA"

    # Tests for skribu_pvk
    def test_skribu_pvk_empty(self, ilo):
        """Test: skribu_pvk of empty word returns empty string"""
        vorto = []
        assert ilo.skribu_pvk(vorto) == ""

    def test_skribu_pvk_one_syllable(self, ilo):
        """Test: skribu_pvk of single syllable"""
        vorto = [Silabo(k="b", v="a")]
        assert ilo.skribu_pvk(vorto) == "AB"

    def test_skribu_pvk_multiple_syllables(self, ilo):
        """Test: skribu_pvk with multiple syllables joined by hyphen"""
        vorto = ilo.dividu_laŭ_pvk("alta")
        assert ilo.skribu_pvk(vorto) == "AL-yT-Ax>"
