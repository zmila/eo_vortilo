import os

# Enumeration for commands
from enum import Enum


class Command(Enum):
    ReadFilesInFolder = 1
    DeleteAddress = 2
    Filtrilo_GrupiguJeklasoj = 3
    Filtrilo_KonvertuTxt2Json = 4
    Filtrilo_ForiguNevalidajnVortojn = 5
    Filtrilo_DetalajFremdaj = 6
    Filtrilo_KuniguKlasojn = 7
    Filtrilo_ForigiMajusklojn = 8
    Filtrilo_AlCSV = 9
    Filtrilo_GrupiguLaŭLongeco = 10
    Analizilo_GrupigiLaŭKlasoj = 11
    Analizilo_TrovuOrfajnFormojn = 12
    Analizilo_Um = 13
    Analizilo_Statistiko3 = 14
    Analizilo_StatistikoKV = 15
    Analizilo_StatistikoKKK = 16


# Global variables
data_folder = "~/prg/java/PseudoTextGenerator/data/input-data"

current_task = (
    Command.Analizilo_Um,
    "/home/dzmitry_laptsionak/prg/java/PseudoTextGenerator/data/output-data/kun_streketoj.yaml",
)


#  final result in
# all_files_vortoj_oftecoj.yml
# all_files_vortoj_oftecoj.csv
#  and
#  all_files_vortoj_oftecoj_radikoj.yml

# dua varianto
# komencinte de tekstoj_kun_streketoj
# nun la rezulto estas en
# "kun_streketoj.yaml"


class TaskExecutor:
    def __init__(self, folder):
        self.folder = fix_folder_name(folder)

    def execute(self, task):
        self.task = task
        file_name = os.path.join(self.folder, self.task[1])

        if self.task[0] == Command.ReadFilesInFolder:
            import iloj.prepar_ilo as prepar_ilo

            prepar_ilo.faru(file_name)

        elif self.task[0] == Command.DeleteAddress:
            import iloj.prepar_ilo as prepar_ilo

            prepar_ilo.delete_addresses(file_name)

        elif self.task[0] == Command.Filtrilo_GrupiguJeklasoj:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.grupigu_je_klasoj(file_name)

        elif self.task[0] == Command.Filtrilo_KonvertuTxt2Json:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.konvertu_txt_je_json(file_name)

        elif self.task[0] == Command.Filtrilo_ForiguNevalidajnVortojn:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.forigu_misvortojn(file_name)

        elif self.task[0] == Command.Filtrilo_DetalajFremdaj:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.detaligu_fremdajn(file_name)

        elif self.task[0] == Command.Filtrilo_KuniguKlasojn:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.kunigu_ĉiujn_klasojn(file_name)

        elif self.task[0] == Command.Filtrilo_ForigiMajusklojn:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.forigi_majusklojn(file_name)

        elif self.task[0] == Command.Filtrilo_AlCSV:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.konvertu_al_csv(file_name)

        elif self.task[0] == Command.Filtrilo_GrupiguLaŭLongeco:
            import iloj.filtr_ilo as filtr_ilo

            filtr_ilo.malgrupigu_laŭ_longeco(file_name)
            # filtr_ilo.grupigu_laŭ_longeco(file_name)

        elif self.task[0] == Command.Analizilo_GrupigiLaŭKlasoj:
            import iloj.analiz_ilo as analiz_ilo

            analiz_ilo.grupigu_laŭ_klasoj(file_name)

        elif self.task[0] == Command.Analizilo_TrovuOrfajnFormojn:
            import iloj.analiz_ilo as analiz_ilo

            analiz_ilo.trovu_orfajn_formojn(file_name)

        elif self.task[0] == Command.Analizilo_Um:
            import iloj.analiz_ilo as analiz_ilo

            # analiz_ilo.grupigu_laŭ_radiko(file_name)
            analiz_ilo.faru_um(file_name)
            # analiz_ilo.konvertu_yml_al_csv(file_name)

        elif self.task[0] == Command.Analizilo_Statistiko3:
            import iloj.analiz_ilo as analiz_ilo

            analiz_ilo.kalkulu_oftecon_de_triopoj(file_name)

        elif self.task[0] == Command.Analizilo_StatistikoKV:
            import iloj.analiz_ilo as analiz_ilo

            analiz_ilo.kalkulu_statistikon_kv(file_name)
            # analiz_ilo.kalkulu_statistikon_laŭ_longeco(file_name)


def fix_folder_name(folder_name):
    path = ""
    if folder_name.startswith("/"):
        path = folder_name
    elif folder_name.startswith("~"):
        path = os.path.expanduser(folder_name)
    else:
        path = os.path.join(os.getcwd(), folder_name)
    return path


# Main method
def main():
    # Get the command from the user
    # command = Command(int(input("Enter command (1 for Ilo1, 2 for Ilo2, etc.): ")))

    executor = TaskExecutor(data_folder)
    executor.execute(current_task)


# Run the main method
if __name__ == "__main__":
    main()
