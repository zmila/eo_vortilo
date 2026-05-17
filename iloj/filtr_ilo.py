from enum import Enum
import re
import time
import json
import locale


class Klaso(Enum):
    A = "a"
    O = "o"
    I = "i"
    E = "e"
    Ŭ = "ŭ"
    NEKONATA = "nenia"
    MALLONGA = "mallonga"
    MALOFTA = "malofta"
    FREMDA = "fremda"
    REKLASIGU = "necesas ree klasigi la vorton"
    KUNE = "ĉiuj klasoj kune"
    KUN_STREKETOJ = "kun streketoj"
    SEN_STREKETOJ = "sen streketoj"


def grupigu_je_klasoj(input_file):
    print(" grupigu_je_klasoj: " + input_file)

    start_time = time.time()
    lines = read_file_to_list(input_file)

    klasoj = {}
    for line in lines:
        vortoj = dividu_per_spaco(line)
        klasi_vortojn(klasoj, vortoj)

    klasoj_sorted = sortigu_klasojn(klasoj)

    write_classes_to_file(klasoj_sorted, input_file + ".klasoj")

    end_time = time.time()
    duration = (end_time - start_time) * 1000
    print(f"Total time: {duration:.2f} ms")


def konvertu_txt_je_json(input_file):
    print(" konvertu_txt_je_json: " + input_file)
    klasoj = read_classes_from_file(input_file)
    write_classes_to_json_file(klasoj, input_file + ".json")


def forigu_misvortojn(input_file):
    print(" forigu_misvortojn: " + input_file)
    klasoj = read_classes_from_json_file(input_file)

    rara_klaso = klasoj.get(Klaso.MALOFTA, {})
    maloftaj = 0

    for _, vortoj in klasoj.items():
        for vorto in list(vortoj.keys()):
            if not valida_vorto(vorto):
                # forigitaj += 1
                del vortoj[vorto]
            if vortoj[vorto] < 5:
                rara_klaso[vorto] = vortoj[vorto]
                maloftaj += 1
                del vortoj[vorto]

    fremdaj = klasoj.get(Klaso.FREMDA, {})
    for vorto in list(fremdaj.keys()):
        if not esperantaj_literoj(vorto):
            # forigitaj += 1
            del vortoj[vorto]

    base, ext = input_file.rsplit(".", 1)
    input_file = f"{base}_validaj.{ext}"
    write_classes_to_json_file(klasoj, input_file)

    print(f"maloftaj (< 5): {maloftaj}")


def trovu_radikon(vorto):
    if len(vorto) <= 3:
        return vorto

    vorto = vorto.replace("_", "")

    suffixes = [
        "ojn",
        "ajn",
        "oj",
        "on",
        "aj",
        "an",
        "os",
        "as",
        "is",
        "us",
        "en",
        "u",
        "o",
        "a",
        "i",
        "e",
    ]
    for suffix in suffixes:
        if vorto.endswith(suffix):
            return vorto[: -len(suffix)]

    return vorto


def forigu_substrekojn(vorto):
    if len(vorto) <= 3:
        return vorto
    
    pattern_before = r"_([aeiou])"
    pattern_after = r"([aeiou])_"

    return re.sub(pattern_after, lambda m: m.group(1),
            re.sub(pattern_before, lambda m: m.group(1), vorto))


def detaligu_fremdajn(input_file):
    print("detaligu_fremdajn: " + input_file)
    klasoj = read_classes_from_json_file(input_file)

    ĉiuj_vortoj = klasoj[Klaso.KUNE]
    sen_finaĵoj = {}
    for vorto, kvanto in ĉiuj_vortoj.items():
        sen_substrekoj = forigu_substrekojn(vorto)
        sen_finaĵoj[sen_substrekoj] = sen_finaĵoj.get(sen_substrekoj, 0) + kvanto

    # kune = {}
    # kune[Klaso.KUNE]=sen_finaĵoj

    base, ext = input_file.rsplit(".", 1)
    output_file = f"{base}.yaml"
    write_classes_to_yaml_file(sen_finaĵoj, output_file)
    
    # laŭ_radikoj = {}
    # for vorto, kvanto in sen_finaĵoj.items():
    #     radiko = trovu_radikon(vorto)
    #     if radiko not in laŭ_radikoj:
    #         laŭ_radikoj[radiko] = []
    #     laŭ_radikoj[radiko].append((vorto, kvanto))

    # base, ext = input_file.rsplit(".", 1)
    # input_file = f"{base}_radikoj.{ext}"
    # write_list_to_json_file(laŭ_radikoj, input_file)


def dividu_laŭ_streketoj(input_file):
    print("detaligu_fremdajn: " + input_file)
    klasoj = read_classes_from_json_file(input_file)
    ĉiuj_vortoj = klasoj[Klaso.KUNE]

    laŭ_streketoj = {}
    laŭ_streketoj[Klaso.KUN_STREKETOJ] = {}
    kun_streketoj = laŭ_streketoj[Klaso.KUN_STREKETOJ]
    laŭ_streketoj[Klaso.SEN_STREKETOJ] = {}
    sen_streketoj = laŭ_streketoj[Klaso.SEN_STREKETOJ]
    for vorto, kvanto in ĉiuj_vortoj.items():
        if "_" in vorto:
            kun_streketoj[vorto] = kvanto
        else:
            sen_streketoj[vorto] = kvanto

    base, ext = input_file.rsplit(".", 1)
    input_file = f"{base}_streketoj.{ext}"
    write_classes_to_json_file(laŭ_streketoj, input_file)


def kunigu_ĉiujn_klasojn(input_file):
    print("kunigu_ĉiujn_klasojn: " + input_file)
    klasoj = read_classes_from_json_file(input_file)

    ĉiuj_kune = {}
    for vortoj in klasoj.values():
        for vorto, kvanto in vortoj.items():
            minuskla = vorto.lower()
            ĉiuj_kune[minuskla] = ĉiuj_kune.get(minuskla, 0) + kvanto

    klasoj.clear()
    klasoj[Klaso.KUNE] = ĉiuj_kune

    write_classes_to_json_file(klasoj, input_file)


def forigi_majusklojn(input_file):
    print("kunigu_ĉiujn_klasojn: " + input_file)
    klasoj = read_classes_from_json_file(input_file)

    vortoj = klasoj[Klaso.KUNE]
    minuskloj = {}
    klasoj[Klaso.KUNE] = minuskloj
    reklasigu = {}
    klasoj[Klaso.REKLASIGU] = reklasigu
    for vorto, kvanto in vortoj.items():
        if any(char.isupper() for char in vorto):
            vorto_minuskle = vorto.lower()
            if vorto_minuskle in minuskloj:
                minuskloj[vorto_minuskle] += kvanto
            else:
                reklasigu[vorto] = kvanto
        else:
            minuskloj[vorto] = kvanto

    base, ext = input_file.rsplit(".", 1)
    output_file = f"{base}_sen_majuskloj.{ext}"
    write_classes_to_json_file(klasoj, output_file)


def konvertu_al_csv(input_file):
    print("konvertu_al_csv: " + input_file)
    klasoj = read_classes_from_json_file(input_file)

    vortoj = klasoj[Klaso.KUNE]

    base, ext = input_file.rsplit(".", 1)
    output_file = f"{base}.csv"
    print(f"Writing to csv file: {output_file}")
    with open(output_file, "w") as f:
        for vorto, kvanto in sorted(
            vortoj.items(), key=lambda item: item[1], reverse=True
        ):
            f.write(f"{vorto},{kvanto}\n")


def grupigu_laŭ_longeco(input_file):
    print("grupigu_laŭ_longeco: " + input_file)
    # read csv file and group words by length
    with open(input_file, "r") as f:
        lines = f.readlines()

    longeco_vortoj = {}
    for line in lines:
        vorto, kvanto = line.strip().split(",")
        longeco = len(vorto)
        vortoj = longeco_vortoj.get(longeco, {})
        vortoj[vorto] = int(kvanto)
        longeco_vortoj[longeco] = vortoj

    # write to yml file
    base, ext = input_file.rsplit(".", 1)
    output_file = f"{base}.yml"
    print(f"Writing to yml file: {output_file}")
    with open(output_file, "w") as f:
        f.write("longeco_vortoj:\n")
        for longeco, vortoj in longeco_vortoj.items():
            f.write(f"  {longeco}:\n")
            for vorto, kvanto in vortoj.items():
                f.write(f"    {vorto}: {kvanto}\n")


def malgrupigu_laŭ_longeco(input_file):
    print("malgrupigu_laŭ_longeco: " + input_file)
    # read yml file with words grouped by length
    # and join all words in one csv file ordered by frequency
    with open(input_file, "r") as f:
        lines = f.readlines()

    vortoj = {}
    for line in lines:
        if line.startswith("    "):
            vorto, kvanto = line.strip().split(": ")
            vortoj[vorto] = int(kvanto)

    base, ext = input_file.rsplit(".", 1)
    output_file = f"{base}.csv"
    print(f"Writing to csv file: {output_file}")
    with open(output_file, "w") as f:
        locale.setlocale(locale.LC_COLLATE, "eo.UTF-8")
        sorted_vortoj = sorted(
            vortoj.items(), key=lambda item: (-item[1], locale.strxfrm(item[0]))
        )
        for vorto, kvanto in sorted_vortoj:
            f.write(f"{vorto},{kvanto}\n")


###############################################
#  implementation of helper functions


def forigu_vortojn_kun_nula_kvanto(vortoj):
    for vorto in list(vortoj.keys()):
        if vortoj[vorto] == 0:
            del vortoj[vorto]


def reklasigu(vorto, kvanto, klasoj):
    klaso = klasi_vorton(vorto)
    samklasaj_vortoj = klasoj.get(klaso, {})
    samklasaj_vortoj[vorto] = samklasaj_vortoj.get(vorto, 0) + kvanto


def sortigu_klasojn(klasoj):
    sorted = {}
    for klaso, vortoj in klasoj.items():
        sortigitaj_vortoj = sortigu_vortojn(vortoj)
        sorted[klaso] = sortigitaj_vortoj
    return sorted


def sortigu_vortojn(vortoj):
    locale.setlocale(locale.LC_COLLATE, "eo.UTF-8")
    # return dict(
    #     sorted(vortoj.items(), key=lambda item: locale.strxfrm(item[0].lower()))
    # )
    return dict(sorted(vortoj.items(), key=lambda item: item[1], reverse=True))


def dividu_per_spaco(line):
    return line.split(" ")


def klasi_vortojn(klasoj, words):
    for word in words:
        if len(word) < 2:
            continue
        klaso = klasi_vorton(word)
        samklasaj_vortoj = klasoj.get(klaso, {})
        samklasaj_vortoj[word] = samklasaj_vortoj.get(word, 0) + 1
        klasoj[klaso] = samklasaj_vortoj


def klasi_vorton(vorto):
    vorto = vorto.lower()
    vorto = vorto.replace("_", "")

    if re.search(r"[^abcĉdefgĝhĥijĵklmnoprsŝtuŭvz_']", vorto):
        return Klaso.FREMDA

    if len(vorto) <= 3:
        return Klaso.MALLONGA

    if vorto.endswith("aŭ") or vorto.endswith("eŭ"):
        return Klaso.Ŭ

    if (
        vorto.endswith("a")
        or vorto.endswith("an")
        or vorto.endswith("aj")
        or vorto.endswith("ajn")
    ):
        return Klaso.A

    if (
        vorto.endswith("o")
        or vorto.endswith("on")
        or vorto.endswith("oj")
        or vorto.endswith("ojn")
    ):
        return Klaso.O

    if estas_verbo(vorto):
        return Klaso.I

    if vorto.endswith("e") or vorto.endswith("en"):
        return Klaso.E
    else:
        return Klaso.NEKONATA


def estas_verbo(vorto):
    return (
        vorto.endswith("i")
        or vorto.endswith("is")
        or vorto.endswith("as")
        or vorto.endswith("os")
        or vorto.endswith("u")
        or vorto.endswith("us")
    )


def read_file_to_list(input_file):
    """
    This function reads a text file and returns its lines as a list.

    Args:
        input_file: The path to the text file.

    Returns:
        A list of lines from the text file.
    """
    with open(input_file, "r") as file:
        lines = file.readlines()

    return [line.strip() for line in lines if line.strip()]


def write_classes_to_file(klasoj, output_file):
    print(f"Writing to file: {output_file}")
    with open(output_file, "w") as f:
        for klaso, vortoj in klasoj.items():
            f.write(f"\n{klaso.name}: {len(vortoj)}\n")
            for vorto, nombro in vortoj.items():
                f.write(f"\t{vorto}: {nombro}\n")

def write_classes_to_yaml_file(vortoj, output_file):
    print(f"Writing to file: {output_file}")
    with open(output_file, "w") as f:
        for vorto, kvanto in sorted(
            vortoj.items(), key=lambda item: item[1], reverse=True
        ):
            f.write(f"{vorto}: {kvanto}\n")


def write_classes_to_json_file(klasoj, output_file):
    print(f"Writing to file: {output_file}")
    with open(output_file, "w") as f:
        json_klasoj = {klaso.name: vortoj for klaso, vortoj in klasoj.items()}
        json.dump(json_klasoj, f, ensure_ascii=False, indent=4)


def write_list_to_json_file(radikoj, output_file):
    print(f"Writing to file: {output_file}")
    with open(output_file, "w") as f:
        for radiko, vortoj in radikoj.items():
            f.write(f"{radiko}: {vortoj}\n")


def read_classes_from_json_file(input_file):
    klasoj = {}
    with open(input_file, "r") as f:
        json_klasoj = json.load(f)
        for klaso, vortoj in json_klasoj.items():
            klasoj[Klaso[klaso]] = vortoj
    return klasoj


def read_classes_from_file(input_file):
    klasoj = {}

    with open(input_file, "r") as file:
        lines = file.readlines()

    klaso = None
    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith("\t"):
            vorto, nombro = line.split(":")
            klasoj[klaso][vorto.strip()] = int(nombro.strip())
        else:
            klaso = Klaso[line.split(":")[0].strip()]
            klasoj[klaso] = {}
    return klasoj


def valida_vorto(vorto):
    return len(vorto) > 1


def esperantaj_literoj(vorto):
    return all(char in "abcĉdefgĝhĥijĵklmnoprsŝtuŭvz_-'" for char in vorto)
