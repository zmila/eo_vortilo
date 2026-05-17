from enum import Enum
import re
import locale


class Klaso(Enum):
    A = "A"
    O = "O"
    I = "I"
    E = "E"
    NENIA = "NENIA"
    ORFOJ = "ORFOJ"


def kalkulu_statistikon_laŭ_longeco(input_file):
    vortoj = read_flat_yml(input_file)

    longecoj = {}
    for vorto, kvanto in vortoj.items():
        longeco = len(vorto)
        longecoj[longeco] = longecoj.get(longeco, 0) + kvanto
        if longeco > 21:
            print(vorto)

    output_file = change_extension(input_file, "longecoj.yml")
    write_plain_yml_file(longecoj, output_file)


def kalkulu_statistikon_kv(input_file):
    print("kalkulu_statistikon_kv: " + input_file)
    vortoj = read_flat_yml(input_file)

    kv_klasoj = {}
    for vorto, kvanto in vortoj.items():
        duopoj = dividu_je_duopoj(vorto)
        for duopo in duopoj:
            kv_klaso = duopo_je_kv_klaso(duopo)
            kv_klasoj[kv_klaso] = kv_klasoj.get(kv_klaso, 0) + kvanto
            if kv_klaso == "V_":
                print(vorto)

    output_file = change_extension(input_file, "kv.yml")
    write_plain_yml_file(kv_klasoj, output_file)


def dividu_je_duopoj(vorto):
    duopoj = []
    # ne kalkulu ŭ kiel literon, ĝi estas parto de aŭ kaj eŭ
    vorto = vorto.replace("ŭ", "")

    if len(vorto) >= 2:
        duopoj.append(f"<{vorto[:1]}")
        for i in range(len(vorto) - 1):
            duopoj.append(vorto[i : i + 2])
        duopoj.append(f"{vorto[-1:]}>")
    return duopoj


def estas_konsonanto(litero):
    return litero in "bcĉdfgĝhĥjĵklmnprsŝtvz"


def estas_vokalo(litero):
    return litero in "aoeui"


def kv_klaso(litero):
    if estas_konsonanto(litero):
        return "K"
    if estas_vokalo(litero):
        return "V"
    return litero


def duopo_je_kv_klaso(duopo):
    s1, s2 = duopo
    return f"{kv_klaso(s1)}{kv_klaso(s2)}"


def kalkulu_oftecon_de_triopoj(input_file):
    ĉiuj = read_flat_yml(input_file)

    ĉiuj_triopoj = {}
    for vorto, kvanto in ĉiuj.items():
        triopoj = dividu_je_triopoj(vorto)
        for triopo in triopoj:
            ĉiuj_triopoj[triopo] = ĉiuj_triopoj.get(triopo, 0) + int(kvanto)

    base, _ = input_file.rsplit(".", 1)
    output_file = f"{base}_triopoj.yml"
    write_plain_yml_file(ĉiuj_triopoj, output_file)


def write_plain_yml_file(klasoj, output_file):
    print(f"Writing to file: {output_file}")
    with open(output_file, "w") as fout:
        sortigita = sorted(klasoj.items(), key=lambda item: -item[1][1])
        for radiko, kvanto in sortigita:
            fout.write(f"{radiko}: {kvanto}\n")


def dividu_je_triopoj(vorto):
    triopoj = []
    if len(vorto) >= 3:
        triopoj.append(f"_{vorto[:2]}")
        for i in range(len(vorto) - 2):
            triopoj.append(vorto[i : i + 3])
        triopoj.append(f"{vorto[-2:]}_")
    return triopoj


def read_flat_yml(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    ĉiuj = {}
    for line in lines:
        vorto, kvanto = line.strip().split(": ")
        ĉiuj[vorto] = int(kvanto)

    return ĉiuj


def konvertu_yml_al_csv(input_file):
    yml = read_flat_yml(input_file)

    base, _ = input_file.rsplit(".", 1)
    output_file = f"{base}.csv"
    print(f"Writing to csv file: {output_file}")
    with open(output_file, "w") as f:
        for vorto, kvanto in sorted(
            yml.items(), key=lambda item: item[1], reverse=True
        ):
            f.write(f"{vorto},{kvanto}\n")


def faru_um(input_file):
    print("faru_um: " + input_file)
    vortoj = read_flat_yml(input_file)

    kgrupoj = {}
    for vorto, kvanto in vortoj.items():
        # k_aroj = trovu_konsonantarojn(vorto)
        k_aroj = trovu_konsonantarojn_sen_lime(vorto)
        for k_aro in k_aroj:
            [num_v, num_ar] = kgrupoj.get(k_aro, [0, 0])
            kgrupoj[k_aro] = [num_v + 1, num_ar + kvanto]

    output_file = change_extension(input_file, "k.yml")
    write_plain_yml_file(kgrupoj, output_file)


# vortoj, literoj: [6050277, 29080552]
# La: [3686, 811111]
# Pro: [990, 63794]


def trovu_konsonantarojn_sen_lime(vorto):
    konsonantaroj = []
    nuna_konsonantaro = ""
    for litero in vorto:
        if estas_konsonanto(litero):
            nuna_konsonantaro += litero
        else:
            konsonantaroj.append([nuna_konsonantaro, litero])
            nuna_konsonantaro = ""

    if len(nuna_konsonantaro) > 0:
        konsonantaroj.append([nuna_konsonantaro, ""])

    if len(konsonantaroj) == 0:
        return konsonantaroj

    konsonantaroj2 = []
    if len(konsonantaroj[0][0]) > 0:
        konsonantaroj2.append(konsonantaroj[0][0])
        
    for i in range(1, len(konsonantaroj)-1):
        k,v = konsonantaroj[i]
        if k == "jn":
            k = "n"
        elif k.startswith("jn"):
            k = k[2:]
        elif len(k) > 1 and k[0] in "ŭjnslmr":
            k = k[1:]

        if len(k) > 0:
            konsonantaroj2.append(k)

    k,v = konsonantaroj[-1]
    if len(k) > 1 and k[0] in "ŭnjslmr":
        konsonantaroj2.append(k[1:])
        
    for k in konsonantaroj2:
        if k == "nt":
            print(vorto)
            break

    return konsonantaroj2


# print(trovu_konsonantarojn_sen_lime("cent"))
# print(trovu_konsonantarojn_sen_lime("suplemente"))
# print(trovu_konsonantarojn_sen_lime("ananean"))
# print(trovu_konsonantarojn_sen_lime("tata"))
# print(trovu_konsonantarojn_sen_lime("tatat"))
# print(trovu_konsonantarojn_sen_lime("rarar"))
# print(trovu_konsonantarojn_sen_lime("rara"))
# print(trovu_konsonantarojn_sen_lime("ntontont"))
# print(trovu_konsonantarojn_sen_lime("stastast"))
# print(trovu_konsonantarojn_sen_lime("stasta"))
# print(trovu_konsonantarojn_sen_lime("jnajnajn"))


def trovu_konsonantarojn(vorto):
    konsonantaroj = []
    nuna_konsonantaro = ""
    for litero in vorto:
        if estas_konsonanto(litero):
            nuna_konsonantaro += litero
        else:
            if len(nuna_konsonantaro) >= 2:
                konsonantaroj.append(nuna_konsonantaro)
            nuna_konsonantaro = ""

    if len(nuna_konsonantaro) >= 2:
        konsonantaroj.append(nuna_konsonantaro)

    if len(konsonantaroj) == 0:
        return konsonantaroj

    if vorto.startswith(konsonantaroj[0]):
        konsonantaroj[0] = "<" + konsonantaroj[0]
    if vorto.endswith(konsonantaroj[-1]):
        konsonantaroj[-1] = konsonantaroj[-1] + ">"

    konsonantaroj2 = []
    for k in konsonantaroj:
        if k.startswith("jn"):
            k = k[2:]
        elif k[0] in "ŭjnslmr":
            k = k[1:]

        if len(k) >= 2:
            konsonantaroj2.append(k)

    return konsonantaroj2


# print(trovu_konsonantarojn("balancis"))


def grupigu_laŭ_radiko(input_file):
    ĉiuj = read_flat_yml(input_file)

    radikoj = {}
    for vorto, kvanto in ĉiuj.items():
        radiko, finaĵo = dividu_vorton(vorto)
        samradikaj = radikoj.get(radiko, {})
        samradikaj[radiko + "_" + finaĵo] = kvanto
        radikoj[radiko] = samradikaj

    statistiko = {}
    for radiko, vortoj in radikoj.items():
        kvanto = 0
        for vorto, kv in vortoj.items():
            kvanto += int(kv)
        statistiko[radiko] = (len(vortoj), kvanto)

    base, _ = input_file.rsplit(".", 1)
    output_file = f"{base}_unikaj_radikoj.yml"
    with open(output_file, "w") as fout:
        sorted_statistiko = sorted(statistiko.items(), key=lambda item: -item[1][1])
        for radiko, (kvanto, sumo) in sorted_statistiko:
            fout.write(f"{radiko}: ({kvanto}, {sumo})\n")

    # base, _ = input_file.rsplit(".", 1)
    # output_file = f"{base}_radikoj.yml"
    # write_yml_file(radikoj, output_file)


def trovu_orfajn_formojn(input_file):
    klasoj = read_classes_from_yml(input_file)

    ĉiuj = {}
    ĉiuj.update(klasoj[Klaso.A])
    ĉiuj.update(klasoj[Klaso.O])
    ĉiuj.update(klasoj[Klaso.E])
    ĉiuj.update(klasoj[Klaso.I])
    ĉiuj.update(klasoj[Klaso.NENIA])

    orfoj = {}
    trovu_orfojn(klasoj[Klaso.A], orfoj, ĉiuj)
    trovu_orfojn(klasoj[Klaso.E], orfoj, ĉiuj)
    trovu_orfojn(klasoj[Klaso.I], orfoj, ĉiuj)
    trovu_orfojn(klasoj[Klaso.O], orfoj, ĉiuj)

    klasoj[Klaso.ORFOJ] = orfoj

    base, _ = input_file.rsplit(".", 1)
    output_file = f"{base}_orfoj.yml"
    write_classes_to_file(klasoj, output_file)


def trovu_orfojn(vortoj, orfoj, ĉiuj):
    for vorto, kvanto in vortoj.items():
        radiko, finaĵo = dividu_vorton(vorto)
        if finaĵo == "" or not havas_samradikajn(radiko, vorto, ĉiuj):
            orfoj[vorto] = kvanto
            vortoj[vorto] = 0
            continue


def havas_samradikan(radiko_finaĵo, vorto, ĉiuj):
    return radiko_finaĵo != vorto and radiko_finaĵo in ĉiuj


def havas_samradikajn(radiko, vorto, ĉiuj):
    return (
        havas_samradikan(radiko + "o", vorto, ĉiuj)
        or havas_samradikan(radiko + "oj", vorto, ĉiuj)
        or havas_samradikan(radiko + "on", vorto, ĉiuj)
        or havas_samradikan(radiko + "ojn", vorto, ĉiuj)
        or havas_samradikan(radiko + "a", vorto, ĉiuj)
        or havas_samradikan(radiko + "aj", vorto, ĉiuj)
        or havas_samradikan(radiko + "an", vorto, ĉiuj)
        or havas_samradikan(radiko + "ajn", vorto, ĉiuj)
        or havas_samradikan(radiko + "e", vorto, ĉiuj)
        or havas_samradikan(radiko + "en", vorto, ĉiuj)
        or havas_samradikan(radiko + "as", vorto, ĉiuj)
        or havas_samradikan(radiko + "is", vorto, ĉiuj)
        or havas_samradikan(radiko + "os", vorto, ĉiuj)
        or havas_samradikan(radiko + "us", vorto, ĉiuj)
        or havas_samradikan(radiko + "u", vorto, ĉiuj)
    )


def dividu_vorton(vorto):
    if vorto.endswith("ajn"):
        return vorto[:-3], "ajn"
    if vorto.endswith("aj"):
        return vorto[:-2], "aj"
    if vorto.endswith("an"):
        return vorto[:-2], "an"
    if vorto.endswith("a"):
        return vorto[:-1], "a"

    if vorto.endswith("ojn"):
        return vorto[:-3], "ojn"
    if vorto.endswith("oj"):
        return vorto[:-2], "oj"
    if vorto.endswith("on"):
        return vorto[:-2], "on"
    if vorto.endswith("o"):
        return vorto[:-1], "o"

    if vorto.endswith("en"):
        return vorto[:-2], "en"
    if vorto.endswith("e"):
        return vorto[:-1], "e"

    if vorto.endswith("as"):
        return vorto[:-2], "as"
    if vorto.endswith("is"):
        return vorto[:-2], "is"
    if vorto.endswith("os"):
        return vorto[:-2], "os"
    if vorto.endswith("us"):
        return vorto[:-2], "us"
    if vorto.endswith("u"):
        return vorto[:-1], "u"
    if vorto.endswith("i"):
        return vorto[:-1], "i"

    return vorto, ""


def read_classes_from_yml(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    klasoj = {}
    klaso = None
    for line in lines:
        if line.startswith("\t"):
            vorto, kvanto = line.strip().split(": ")
            samklasaj_vortoj = klasoj.get(klaso, {})
            samklasaj_vortoj[vorto] = kvanto
            klasoj[klaso] = samklasaj_vortoj
        elif " " in line:
            nomo_de_klaso, _ = line.strip().split(" ")
            klaso = Klaso(nomo_de_klaso)
        else:
            print("error! line without space: " + line)

    return klasoj


def grupigu_laŭ_klasoj(input_file):
    # read csv file and group words by class
    with open(input_file, "r") as f:
        lines = f.readlines()

    klasoj = {}
    for line in lines:
        vorto, kvanto = line.strip().split(",")
        klaso = klasi_vorton(vorto)
        samklasaj_vortoj = klasoj.get(klaso, {})
        samklasaj_vortoj[vorto] = kvanto
        klasoj[klaso] = samklasaj_vortoj

    # write to yml file
    output_file = change_extension(input_file, "yml")
    write_classes_to_file(klasoj, output_file)


def write_yml_file(klasoj, output_file):
    print(f"Writing to file: {output_file}")
    locale.setlocale(locale.LC_COLLATE, "eo.UTF-8")

    with open(output_file, "w") as f:
        for klaso, vortoj in klasoj.items():
            f.write(f"\n{klaso} {len(vortoj)}:\n")
            sorted_vortoj = sorted(
                vortoj.items(),
                key=lambda item: (-int(item[1]), locale.strxfrm(item[0])),
            )
            for vorto, kvanto in sorted_vortoj:
                f.write(f"\t{vorto}: {kvanto}\n")


def write_classes_to_file(klasoj, output_file):
    print(f"Writing to file: {output_file}")
    locale.setlocale(locale.LC_COLLATE, "eo.UTF-8")

    with open(output_file, "w") as f:
        for klaso, vortoj in klasoj.items():
            f.write(f"\n{klaso.name} {len(vortoj)}:\n")
            sorted_vortoj = sorted(
                vortoj.items(),
                key=lambda item: (-int(item[1]), locale.strxfrm(item[0])),
            )
            for vorto, kvanto in sorted_vortoj:
                f.write(f"\t{vorto}: {kvanto}\n")


def change_extension(file_name, new_ext):
    base, _ = file_name.rsplit(".", 1)
    return f"{base}.{new_ext}"


def klasi_vorton(vorto):
    vorto = vorto.lower()
    if re.search(r"[^abcĉdefgĝhĥijĵklmnoprsŝtuŭvz]", vorto):
        return Klaso.FREMDA
    if len(vorto) <= 2:
        return Klaso.NENIA
    if (
        vorto.endswith("a")
        or vorto.endswith("an")
        or vorto.endswith("aj")
        or vorto.endswith("ajn")
    ):
        return Klaso.A
    elif (
        vorto.endswith("o")
        or vorto.endswith("on")
        or vorto.endswith("oj")
        or vorto.endswith("ojn")
    ):
        return Klaso.O
    elif estas_verbo(vorto):
        return Klaso.I
    elif vorto.endswith("e") or vorto.endswith("en"):
        return Klaso.E
    else:
        return Klaso.NENIA


def estas_verbo(vorto):
    return (
        vorto.endswith("i")
        or vorto.endswith("is")
        or vorto.endswith("as")
        or vorto.endswith("os")
        or vorto.endswith("u")
        or vorto.endswith("us")
    )
