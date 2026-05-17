import re
from typing import TypedDict

NUL_KO = '∅'


class Silabo(TypedDict):
    k: str
    v: str
    f: str


Vorto = list[Silabo]


class KevakIlo:
    """Class for breaking Esperanto text into syllables (kevako method)."""

    def _estas_vokalo(self, char: str) -> bool:
        return char in 'aeiou'

    def _estas_konsonanto(self, char: str) -> bool:
        return char in 'bcĉdfgĝhĥjĵklmnprsŝtŭvz'

    def _teksto_al_vortoj(self, text: str) -> list[str]:
        cleaned = re.sub(r'[,.!?;:()\"\[\]{}…—–]', '', text)
        return [w for w in cleaned.split() if w]

    def _trovi_disigan_indekson(self, konsonanta_areto: str) -> int:
        length = len(konsonanta_areto)
        if length == 3:
            return 2
        elif length == 4:
            return 2
        else:
            return 1

    def _prilabori_intervokalojn(self, nuna_k: str, silaboj: list[Silabo]) -> str:
        if nuna_k == 'ŭ' and silaboj and self._estas_vokalo(silaboj[-1]['v']):
            silaboj[-1]['f'] = 'ŭ'
            return ''

        if len(nuna_k) > 1:
            disiga_indekso = self._trovi_disigan_indekson(nuna_k)
            lasta_silabo = silaboj[-1]
            lasta_silabo['f'] = nuna_k[:len(nuna_k) - disiga_indekso]
            return nuna_k[len(nuna_k) - disiga_indekso:]

        return nuna_k

    def _finu_silabon(self, nuna_k: str, silaboj: list[Silabo]) -> None:
        if nuna_k and silaboj:
            silaboj[-1]['f'] = nuna_k
        elif nuna_k:
            silaboj.append({'k': nuna_k, 'v': '', 'f': ''})

    def _vorto_al_silaboj(self, vorto_text: str) -> Vorto:
        silaboj: list[Silabo] = []
        nuna_k = ''
        post_limo = False  # True after an explicit syllable boundary (-, ', _)

        for char in vorto_text:
            if char in ("-", "'", "_"):
                self._finu_silabon(nuna_k, silaboj)
                nuna_k = ''
                post_limo = True
                continue

            if self._estas_vokalo(char):
                if silaboj and nuna_k and not post_limo:
                    nuna_k = self._prilabori_intervokalojn(nuna_k, silaboj)
                silaboj.append({'k': nuna_k, 'v': char, 'f': ''})
                nuna_k = ''
                post_limo = False
            elif self._estas_konsonanto(char):
                nuna_k += char

        self._finu_silabon(nuna_k, silaboj)
        return silaboj

    def dividuJeSilaboj(self, text: str) -> list[Vorto]:
        if not text:
            return []
        vortoj_text = self._teksto_al_vortoj(text.lower())
        return [self._vorto_al_silaboj(v) for v in vortoj_text]

    def _formatigi_silabon(self, s: Silabo) -> str:
        k = s['k'] or NUL_KO
        if s['f']:
            return f"({k}|{s['v']}|{s['f']})"
        return f"({k}|{s['v']})"

    def formatigi(self, vortoj: list[Vorto]) -> str:
        if not vortoj:
            return ''
        return ' '.join(
            '-'.join(self._formatigi_silabon(s) for s in vorto)
            for vorto in vortoj
        )

    def _skribu_silabon(self, s: Silabo) -> str:
        result = ''
        if s['k']:
            result += s['k']
        result += s['v']
        if s['f']:
            result += s['f']
        return result

    def skribu(self, vortoj: list[Vorto]) -> str:
        if not vortoj:
            return ''
        return ' '.join(
            ''.join(self._skribu_silabon(s) for s in vorto)
            for vorto in vortoj
        )

