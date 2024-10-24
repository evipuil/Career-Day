import pandas
import csv

students_file = pandas.read_csv("students copy.csv")
sessions_file = pandas.read_csv("sessions copy.csv")
max_students = 25
min_students = 15

students = {}
timestamp_delta = max(list(students_file["TIMESTAMP"])) - min(list(students_file["TIMESTAMP"]))
min_time = min(list(students_file["TIMESTAMP"]))

for a in range(len(students_file)):
    students[students_file[" ID"][a]] = {
        "FIRST_NAME": students_file[" FIRST_NAME"][a].strip(),
        "LAST_NAME": students_file[" LAST_NAME"][a].strip(),
        "HOMEROOM": students_file[" HOMEROOM"][a].strip(),
        "FIRST_PERIOD": students_file[" FIRST_PERIOD"][a].strip(),
        "ID": students_file[" ID"][a],
        "GRADE": students_file[" GRADE"][a],
        "CHOICE_1": [students_file[" CHOICE_1"][a], False],
        "CHOICE_2": [students_file[" CHOICE_2"][a], False],
        "CHOICE_3": [students_file[" CHOICE_3"][a], False],
        "CHOICE_4": [students_file[" CHOICE_4"][a], False],
        "CHOICE_5": [students_file[" CHOICE_5"][a], False],
        "CHOICE_6": [students_file[" CHOICE_6"][a], False],
        "CHOICE_7": [students_file[" CHOICE_7"][a], False],
        "PERIOD_1": 0,
        "PERIOD_2": 0,
        "PERIOD_3": 0,
        "PERIOD_4": 0,
        "PRIORITY": (int(students_file[" GRADE"][a]) - 6) + (1 - (int(students_file["TIMESTAMP"][a]) - min_time) / timestamp_delta),
        "FILLED": 0,
        "TRIED": 0
    }

sorted_students = dict(sorted(students.items(), key=lambda item: item[1]["PRIORITY"], reverse=True))
ids = list(sorted_students.keys())

sessions = {}
for b in range(len(sessions_file)):
    sessions[sessions_file["ID"][b]] = {
        "SUBJECT": sessions_file[" Subject"][b].strip(),
        "TEACHER": sessions_file[" Teacher"][b].strip(),
        "PRESENTER": sessions_file[" Presenter"][b].strip(),
        "STUDENTS": 0
    }
session_values = list(sessions.values())
session_ids = list(sessions.keys())

random = []
complete = 0
bad = 0
good = 0 
medium = 0
for c in range(1, 5):
    for d in range(len(sorted_students)):
        student = ids[d]
        for e in range(1, 8):
            try:
                if sessions[sorted_students[student]["CHOICE_" + str(e)][0]]["STUDENTS"] < max_students and sorted_students[student]["CHOICE_" + str(e)][1] == False:
                    sessions[sorted_students[student]["CHOICE_" + str(e)][0]]["STUDENTS"] += 1
                    sorted_students[student]["CHOICE_" + str(e)][1] = True
                    sorted_students[student]["PERIOD_" + str(c)] = sorted_students[student]["CHOICE_" + str(e)][0]
                    sorted_students[student]["PRIORITY"] -= 0.5
                    good += 1
                    break
            except:
                sorted_students[student]["PERIOD_" + str(c)] = session_ids[0]
                sessions[session_ids[0]]["STUDENTS"] += 1
                bad += 1
                break
        if sorted_students[student]["PERIOD_" + str(c)] == 0:
            for f in range(len(sessions)):
                if sessions[session_ids[f]]["STUDENTS"] < max_students:
                    sorted_students[student]["PERIOD_" + str(c)] = f + 1
                    sessions[session_ids[f]]["STUDENTS"] += 1
                    medium += 1
                    break
            sorted_students[student]["PRIORITY"] += 0.5
        sorted_students = dict(sorted(students.items(), key=lambda item: item[1]["PRIORITY"], reverse=True))
        sessions = dict(sorted(sessions.items(), key=lambda x: x[1]["STUDENTS"]))
        session_ids = list(sessions.keys())
        session_values = list(sessions.values())
    for g in range(len(sessions)):
        if sessions[session_ids[g]]["STUDENTS"] < min_students:
            print("Session " + str(g + 1) + " does not have enough students.")
            print("Students: ", sessions[session_ids[g]]["STUDENTS"])
        sessions[session_ids[g]]["STUDENTS"] = 0
print("Bad: ", bad, "Medium: ", medium, "Good: ", good, "Total: ", len(sorted_students))

print(sorted_students)
ids = list(sorted_students.keys())
f = open("output.csv", "w", newline="")
writer = csv.writer(f)
writer.writerow(["NUM_STUDENTS", len(sorted_students)])
writer.writerow(["FIRST_NAME", "LAST_NAME", "HOMEROOM", "FIRST_PERIOD", "GRADE", "SESS_1_ID", "SESS_1_ROOM", "SESS_2_ID", "SESS_2_ROOM", "SESS_3_ID", "SESS_3_ROOM", "SESS_4_ID", "SESS_4_ROOM"])

for e in range(len(sorted_students)):
    student = ids[e]
    try:
        writer.writerow([sorted_students[student]["FIRST_NAME"], 
                        sorted_students[student]["LAST_NAME"], 
                        sorted_students[student]["HOMEROOM"], 
                        sorted_students[student]["FIRST_PERIOD"], 
                        sorted_students[student]["ID"],
                        sorted_students[student]["GRADE"], 
                        int(sorted_students[student]["PERIOD_1"]), 
                        sessions[sorted_students[student]["PERIOD_1"]]["TEACHER"], 
                        int(sorted_students[student]["PERIOD_2"]), 
                        sessions[sorted_students[student]["PERIOD_2"]]["TEACHER"], 
                        int(sorted_students[student]["PERIOD_3"]), 
                        sessions[sorted_students[student]["PERIOD_3"]]["TEACHER"], 
                        int(sorted_students[student]["PERIOD_4"]), 
                        sessions[sorted_students[student]["PERIOD_4"]]["TEACHER"]])
    except:
        print("BAD")
f.close()