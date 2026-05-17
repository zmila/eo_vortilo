from typing import NamedTuple

NUL_KO = "x"
NUL_VO = "y"
SKIP_CHARS = {"'", "_", "-"}


class Silabo(NamedTuple):
    """Immutable syllable record with consonant (k) and vowel (v) components."""
    k: str
    v: str


Vorto = list[Silabo]


class DuLiteraSilabiIlo:
    """Class for breaking Esperanto text into two-letter syllables either VC or CV modes,
    using help (unprononced) consonant `x` and vowel `y` to form full two letter syllables."""

    def dividu_laŭ_avk(self, vorto: str) -> list[Silabo]:
        """Divide a word into two-letter syllables in AVK (antaŭ-vokala konsonanto) mode.

        Each syllable is KV (consonant-vowel):
        - If a vowel has no consonant before it, add NUL_KO (x)
        - If a consonant has no vowel after it, add NUL_VO (y)
        - Skip characters: ', _, - (visual dividers, not part of syllables)
        """
        if not vorto:
            return []

        vorto_lc = vorto.lower()
        vorto_lc = "".join(c for c in vorto_lc if c not in SKIP_CHARS)
        
        vokaloj = {"a", "e", "i", "o", "u"}
        silaboj = []

        i = 0
        while i < len(vorto_lc):
            char = vorto_lc[i]

            if char in vokaloj:
                # Vowel without consonant - add NUL_KO
                silaboj.append(Silabo(k=NUL_KO, v=char))
                i += 1
            else:
                # Consonant - find or create a vowel
                k = char
                i += 1

                # Look for the next vowel
                if i < len(vorto_lc) and vorto_lc[i] in vokaloj:
                    v = vorto_lc[i]
                    i += 1
                else:
                    # No vowel follows - use NUL_VO
                    v = NUL_VO

                silaboj.append(Silabo(k=k, v=v))

        return silaboj

    def dividu_laŭ_pvk(self, vorto: str) -> list[Silabo]:
        """Divide a word into two-letter syllables in PVK (post-vowel consonant) mode.

        Each syllable is VC (vowel-consonant), but stored as Silabo with:
        - k = consonant (or NUL_KO if no consonant)
        - v = vowel (or NUL_VO if no vowel)
        - Skip characters: ', _, - (visual dividers, not part of syllables)
        """
        if not vorto:
            return []

        vorto_lc = vorto.lower()
        vorto_lc = "".join(c for c in vorto_lc if c not in SKIP_CHARS)
        
        vokaloj = {"a", "e", "i", "o", "u"}
        silaboj = []

        i = 0
        while i < len(vorto_lc):
            char = vorto_lc[i]

            if char in vokaloj:
                # Vowel - look for consonant after it
                v = char
                i += 1

                # Look for the next consonant
                if i < len(vorto_lc) and vorto_lc[i] not in vokaloj:
                    k = vorto_lc[i]
                    i += 1
                else:
                    # No consonant follows - use NUL_KO
                    k = NUL_KO

                silaboj.append(Silabo(k=k, v=v))
            else:
                # Consonant without vowel - use NUL_VO
                k = char
                v = NUL_VO
                i += 1

                silaboj.append(Silabo(k=k, v=v))

        return silaboj

    def skribu_silabon_avk(self, silabo: Silabo) -> str:
        """Convert a single syllable to KV string (AVK mode).

        Silabo always has k=consonant (or NUL_KO), v=vowel (or NUL_VO).
        Rules:
        - NUL_KO (x) and NUL_VO (y) remain lowercase
        - All other consonants and vowels are uppercase

        Example: Silabo(k='x', v='a') → 'xA' (KV order)
        """
        k_str = silabo.k if silabo.k in (NUL_KO, NUL_VO) else silabo.k.upper()
        v_str = silabo.v if silabo.v in (NUL_KO, NUL_VO) else silabo.v.upper()
        return k_str + v_str

    def skribu_silabon_pvk(self, silabo: Silabo) -> str:
        """Convert a single syllable to VC string (PVK mode).

        Silabo always has k=consonant (or NUL_KO), v=vowel (or NUL_VO).
        Rules:
        - NUL_KO (x) and NUL_VO (y) remain lowercase
        - All other consonants and vowels are uppercase

        Example: Silabo(k='l', v='a') → 'AL' (VC order)
        """
        k_str = silabo.k if silabo.k in (NUL_KO, NUL_VO) else silabo.k.upper()
        v_str = silabo.v if silabo.v in (NUL_KO, NUL_VO) else silabo.v.upper()
        return v_str + k_str  # VC order for PVK

    def skribu_avk(self, vorto: Vorto) -> str:
        """Convert a word to KV string representation (AVK mode).

        Syllables are formatted with skribu_silabon_avk and joined with '-' separator.

        Example: [Silabo(k='x', v='a'), Silabo(k='l', v='y'), Silabo(k='t', v='a')] → 'xA-Ly-TA'
        """
        return "-".join(self.skribu_silabon_avk(silabo) for silabo in vorto)

    def skribu_pvk(self, vorto: Vorto) -> str:
        """Convert a word to VC string representation (PVK mode).

        Syllables are formatted with skribu_silabon_pvk and joined with '-' separator.

        Example: [Silabo(k='x', v='a'), Silabo(k='l', v='a'), Silabo(k='t', v='y')] → 'Ax-AL-yT'
        """
        return "-".join(self.skribu_silabon_pvk(silabo) for silabo in vorto)
