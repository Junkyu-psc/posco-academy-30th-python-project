def cal_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'


def show(sorted_stu_lst):
    max_name_len = max((len(stu[1]) for stu in sorted_stu_lst), default=10)

    print(" "*3 + "Student" + " "*max_name_len + "Name" + " "*3 +
          "Midterm" + " "*3 + "Final" + " "*3 + "Average" + " "*3 + "Grade" + " "*2)
    print("-"*(52+max_name_len))
    for student in sorted_stu_lst:
        print(f"{' '*2}{student[0]}", end='')
        print(f"{' '*(4+max_name_len-len(student[1]))}{student[1]}", end='')
        print(f"{' '*6}{student[2]}{' '*7}{student[3]}{' '*6}{student[4]}{' '*6}{student[5]}{' '*4}")
    print()


def changed_show(cnt_stu, ched_stu):
    max_name_len = max(len(stu[1]) for stu in cnt_stu)

    print(" "*3 + "Student" + " "*max_name_len + "Name" + " "*3 +
          "Midterm" + " "*3 + "Final" + " "*3 + "Average" + " "*3 + "Grade" + " "*2)
    print("-"*(52+max_name_len))

    for stu in [cnt_stu[0], ched_stu[0]]:
        print(f"{' '*2}{stu[0]}", end='')
        print(f"{' '*(4+max_name_len-len(stu[1]))}{stu[1]}", end='')
        print(f"{' '*6}{stu[2]}{' '*7}{stu[3]}{' '*6}{stu[4]}{' '*6}{stu[5]}{' '*4}")
        if stu == cnt_stu[0]:
            print("Score changed.")
    print()


def check_student(stu_num, stu_dict):
    if stu_num not in stu_dict:
        print("NO SUCH PERSON.\n")
        return False
    return True


def search(sorted_sl, stu_dict):
    stu_num = input("Student ID: ")
    if not check_student(stu_num, stu_dict):
        return
    for st in sorted_sl:
        if st[0] == stu_num:
            show([st])
            break


def changescore(sorted_sl, stu_dict):
    stu_num = input("Student ID: ")
    if not check_student(stu_num, stu_dict):
        return sorted_sl, stu_dict

    exam = input("Mid/Final? ").lower()
    if exam not in ['mid', 'final']:
        print()
        return sorted_sl, stu_dict

    new_score = int(input("Input new score: "))
    if not (0 <= new_score <= 100):
        print()
        return sorted_sl, stu_dict

    for stu in sorted_sl:
        if stu[0] == stu_num:
            cnt_stu = list(stu)

    cnt_mid, cnt_final = stu_dict[stu_num][1], stu_dict[stu_num][2]
    if exam == 'mid':
        cnt_mid = new_score
    else:
        cnt_final = new_score

    avg_score = (cnt_mid + cnt_final) / 2
    cnt_grade = cal_grade(avg_score)

    stu_dict[stu_num] = [stu_dict[stu_num][0], cnt_mid, cnt_final, avg_score, cnt_grade]

    for i, stu in enumerate(sorted_sl):
        if stu[0] == stu_num:
            sorted_sl[i] = [stu_num, stu_dict[stu_num][0], cnt_mid, cnt_final, avg_score, cnt_grade]

    sorted_sl = sorted(sorted_sl, key=lambda a: a[4], reverse=True)

    for stu in sorted_sl:
        if stu[0] == stu_num:
            ched_stu = list(stu)
            break

    changed_show([cnt_stu], [ched_stu])
    return sorted_sl, stu_dict


def add(sorted_sl, stu_dict):
    stu_num = input("Student ID: ")
    if stu_num in stu_dict:
        print("ALREADY EXISTS.\n")
        return sorted_sl, stu_dict
    if len(stu_num) != 8:
        print("Student ID must be 8 digits.\n")
        return sorted_sl, stu_dict

    stu_name = input("Name: ")
    cnt_mid = int(input("Midterm Score: "))
    cnt_final = int(input("Final Score: "))
    avg_score = (cnt_mid + cnt_final) / 2
    grade = cal_grade(avg_score)

    stu_dict[stu_num] = [stu_name, cnt_mid, cnt_final, avg_score, grade]
    sorted_sl.append([stu_num, stu_name, cnt_mid, cnt_final, avg_score, grade])
    sorted_sl = sorted(sorted_sl, key=lambda a: a[4], reverse=True)

    print("Student added.\n")
    return sorted_sl, stu_dict


def searchgrade(sorted_sl):
    search_grade = input("Grade to search: ").upper()
    if search_grade not in ['A', 'B', 'C', 'D', 'F']:
        print()
        return

    found = [stu for stu in sorted_sl if stu[5] == search_grade]
    if not found:
        print("NO RESULTS.\n")
        return

    show(found)


def remove(sorted_sl, stu_dict):
    stu_num = input("Student ID: ")
    if stu_num not in stu_dict:
        print("NO SUCH PERSON.\n")
        return sorted_sl, stu_dict

    sorted_sl = [stu for stu in sorted_sl if stu[0] != stu_num]
    del stu_dict[stu_num]
    print("Student removed.\n")
    return sorted_sl, stu_dict


def save_file(sorted_sl):
    file_name = input("File name: ")
    with open(file_name, 'w') as f:
        for stu in sorted_sl:
            f.write("\t".join(map(str, stu[:4])) + "\n")


def main():
    import sys
    open_file_name = sys.argv[1] if len(sys.argv) > 1 else "students.txt"

    with open(open_file_name, 'r') as f:
        stu_dict = {}
        sorted_sl = []
        for line in f:
            t = line.strip().split("\t")
            mid, final = int(t[2]), int(t[3])
            avg = (mid + final) / 2
            grade = cal_grade(avg)
            stu_dict[t[0]] = [t[1], mid, final, avg, grade]
            sorted_sl.append([t[0], t[1], mid, final, avg, grade])

    sorted_sl = sorted(sorted_sl, key=lambda a: a[4], reverse=True)
    show(sorted_sl)

    while True:
        cmd = input("# Type command : ").lower()
        if cmd == 'show':
            show(sorted_sl)
        elif cmd == 'search':
            search(sorted_sl, stu_dict)
        elif cmd == 'changescore':
            sorted_sl, stu_dict = changescore(sorted_sl, stu_dict)
        elif cmd == 'add':
            sorted_sl, stu_dict = add(sorted_sl, stu_dict)
        elif cmd == 'searchgrade':
            searchgrade(sorted_sl)
        elif cmd == 'remove':
            if not sorted_sl:
                print("List is empty.\n")
            else:
                sorted_sl, stu_dict = remove(sorted_sl, stu_dict)
        elif cmd == 'quit':
            if input("Save data?[yes/no] ").lower() == 'yes':
                save_file(sorted_sl)
            break
        else:
            print('Available commands: show, search, changescore, searchgrade, add, remove, quit\n')
            continue


if __name__ == "__main__":
    main()
