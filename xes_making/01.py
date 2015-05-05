# NB: data in csv file must be in format "user_id,step_id,step_type,action,timestamp"
# ORDERED BY user_id, timestamp
# timestamp example: "2014-10-25T17:00:27.000+03:00"
def make_simple_xes(source_file_name, result_file_name):
    # result_file_name = "01.xes"
    with open(result_file_name, 'w') as xes_file:
        xes_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xes_file.write("<log xes.version=\"1.0\" xmlns=\"http://www.xes-standard.org\" xes.creator=\"LENA\">\n")

        # EXTENSIONS
        xes_file.write("\t<extension name=\"Concept\" prefix=\"concept\" uri=\"http://www.xes-standard.org/concept.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Lifecycle\" prefix=\"lifecycle\" uri=\"http://www.xes-standard.org/lifecycle.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Time\" prefix=\"time\" uri=\"http://www.xes-standard.org/time.xesext\"/>\n")

        # GLOBALS
        # trace has to have "concept:name" attribute
        xes_file.write("\t" + "<global scope=\"trace\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t"
                          "</global>\n")
        # event has to have "concept:name", "time:timestamp", "step_no", "action" and "step_type" attributes
        xes_file.write("\t" + "<global scope=\"event\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t\t"
                              # "<string key=\"lifecycle:transition\" value=\"transition\"/>\n\t\t"     # useless?
                              "<date key=\"time:timestamp\" value=\"201-01-24T15:53:11.668+02:00\"/>\n\t\t"
                              "<string key=\"step_no\" value=\"string\"/>\n\t\t"
                              "<string key=\"action\" value=\"string\"/>\n\t\t"
                              "<string key=\"step_type\" value=\"string\"/>\n\t"
                          "</global>\n")

        # CLASSIFIERS
        xes_file.write("\t" + "<classifier name=\"Activity\" keys=\"step_no action\"/>\n")
        xes_file.write("\t" + "<classifier name=\"Activity\" keys=\"step_no\"/>\n")
        xes_file.write("\t" + "<classifier name=\"Activity\" keys=\"step_type action\"/>\n")

        # some another stuff
        xes_file.write("\t" + "<string key=\"lifecycle:model\" value=\"standard\"/>\n")

        def make_row(attr_type, key, value):
            return "<{0} key=\"{1}\" value=\"{2}\"/>\n".format(attr_type, key, value)

        def write_event(content, tab):
            xes_file.write(tab + "<event>\n")
            tab += "\t"
            for row in content:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            tab = tab[:-1]
            xes_file.write(tab + "</event>\n")

        def write_trace(properties, events, tab="\t"):
            xes_file.write(tab + "<trace>\n")
            tab += "\t"
            for row in properties:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            for event in events:
                write_event(event, tab)
            tab = tab[:-1]
            xes_file.write(tab + "</trace>\n")

        # NB: data in csv file must be in format "user_id,step_id,step_type,action,timestamp"
        # ORDERED BY user_id, timestamp
        # timestamp example: "2014-10-25T17:00:27.000+03:00"
        with open(source_file_name, 'r') as csv_file:
            cur_user_id = -1
            trace_properties = []
            trace_events = []
            for line in csv_file:
                line = line[:-1]        # end of line character
                user_id, step_no, step_type, action, timestamp = line.split(',')

                if cur_user_id != user_id:
                    # new user !
                    # ??? do we need events "Start\\Start" and "End\\End"
                    if cur_user_id != -1:
                        write_trace(trace_properties, trace_events)
                    trace_properties = [["string", "concept:name", user_id]]
                    trace_events = []
                    cur_user_id = user_id

                """ EXAMPLE (from Disco):
                    <string key="concept:name" value="12252:VIEWED"/>
                    <string key="lifecycle:transition" value="complete"/>       # useless ?
                    <date key="time:timestamp" value="2014-10-25T17:00:27.000+03:00"/>
                    <string key="step_no" value="12252"/>
                    <string key="action" value="VIEWED"/>
                """

                new_event = []
                new_event.append(["string", "concept:name", "".join([step_no, "_", step_type, "\\", action])])
                new_event.append(["date", "time:timestamp", timestamp])
                new_event.append(["string", "step_no", step_no])
                new_event.append(["string", "step_type", step_type])
                new_event.append(["string", "action", action])
                trace_events.append(new_event)
            write_trace(trace_properties, trace_events)

        xes_file.write("</log>\n")

def make_xes_quiz_type(source_file_name, result_file_name):
    # result_file_name = "01.xes"
    with open(result_file_name, 'w') as xes_file:
        xes_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xes_file.write("<log xes.version=\"1.0\" xmlns=\"http://www.xes-standard.org\" xes.creator=\"LENA\">\n")

        # EXTENSIONS
        xes_file.write("\t<extension name=\"Concept\" prefix=\"concept\" uri=\"http://www.xes-standard.org/concept.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Lifecycle\" prefix=\"lifecycle\" uri=\"http://www.xes-standard.org/lifecycle.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Time\" prefix=\"time\" uri=\"http://www.xes-standard.org/time.xesext\"/>\n")

        # GLOBALS
        # trace has to have "concept:name" attribute
        xes_file.write("\t" + "<global scope=\"trace\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t"
                          "</global>\n")
        # event has to have "concept:name", "time:timestamp", "step_no", "action" and "step_type" attributes
        # columns = ["step_no_old", "step_no", "action", "step_type", "quiz_type", "time:timestamp", "student_id"]
        xes_file.write("\t" + "<global scope=\"event\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t\t"     # в данном случае step_type
                              "<date key=\"time:timestamp\" value=\"201-01-24T15:53:11.668+02:00\"/>\n\t\t"
                              "<string key=\"step_no\" value=\"string\"/>\n\t\t"
                              "<string key=\"action\" value=\"string\"/>\n\t\t"
                              "<string key=\"quiz_type\" value=\"string\"/>\n\t"
                          "</global>\n")

        # CLASSIFIERS
        xes_file.write("\t" + "<classifier name=\"Activity1\" keys=\"quiz_type\"/>\n")

        # some other stuff
        xes_file.write("\t" + "<string key=\"lifecycle:model\" value=\"standard\"/>\n")

        def make_row(attr_type, key, value):
            return "<{0} key=\"{1}\" value=\"{2}\"/>\n".format(attr_type, key, value)

        def write_event(content, tab):
            xes_file.write(tab + "<event>\n")
            tab += "\t"
            for row in content:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            tab = tab[:-1]
            xes_file.write(tab + "</event>\n")

        def write_trace(properties, events, tab="\t"):
            xes_file.write(tab + "<trace>\n")
            tab += "\t"
            for row in properties:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            for event in events:
                write_event(event, tab)
            tab = tab[:-1]
            xes_file.write(tab + "</trace>\n")

        # NB: data in csv file must be in format "step_no_old", "step_no", "action", "step_type", "quiz_type", "time:timestamp", "student_id"
        # ORDERED BY user_id, timestamp
        # timestamp example: "2014-10-25T17:00:27.000+03:00"
        with open(source_file_name, 'r') as csv_file:
            cur_user_id = -1
            trace_properties = []
            trace_events = []
            for line in csv_file:
                line = line[:-1]        # end of line character
                # user_id, step_no, step_type, action, timestamp = line.split(',')
                _, step_no, action, step_type, quiz_type, timestamp, user_id = line.split(',')

                if cur_user_id != user_id:
                    # new user !
                    # ??? do we need events "Start\\Start" and "End\\End"
                    if cur_user_id != -1:
                        write_trace(trace_properties, trace_events)
                    trace_properties = [["string", "concept:name", user_id]]
                    trace_events = []
                    cur_user_id = user_id

                new_event = []
                new_event.append(["string", "concept:name", quiz_type])
                new_event.append(["date", "time:timestamp", timestamp])
                new_event.append(["string", "step_no", step_no])
                new_event.append(["string", "action", action])
                new_event.append(["string", "quiz_type", quiz_type])
                trace_events.append(new_event)
            write_trace(trace_properties, trace_events)

        xes_file.write("</log>\n")

def make_xes_quiz_type_and_video(source_file_name, result_file_name, with_actions = False):
    # result_file_name = "01.xes"
    with open(result_file_name, 'w') as xes_file:
        xes_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xes_file.write("<log xes.version=\"1.0\" xmlns=\"http://www.xes-standard.org\" xes.creator=\"LENA\">\n")

        # EXTENSIONS
        xes_file.write("\t<extension name=\"Concept\" prefix=\"concept\" uri=\"http://www.xes-standard.org/concept.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Lifecycle\" prefix=\"lifecycle\" uri=\"http://www.xes-standard.org/lifecycle.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Time\" prefix=\"time\" uri=\"http://www.xes-standard.org/time.xesext\"/>\n")

        # GLOBALS
        # trace has to have "concept:name" attribute
        xes_file.write("\t" + "<global scope=\"trace\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t"
                          "</global>\n")
        # event has to have "concept:name", "time:timestamp", "step_no", "action" and "step_type" attributes
        # columns = ["step_no_old", "step_no", "action", "step_type", "quiz_type", "time:timestamp", "student_id"]
        xes_file.write("\t" + "<global scope=\"event\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t\t"
                              "<date key=\"time:timestamp\" value=\"201-01-24T15:53:11.668+02:00\"/>\n\t\t"
                              #"<string key=\"step_no\" value=\"string\"/>\n\t\t"
                              #"<string key=\"action\" value=\"string\"/>\n\t\t"
                              #"<string key=\"quiz_type\" value=\"string\"/>\n\t"
                          "</global>\n")

        # CLASSIFIERS
        xes_file.write("\t" + "<classifier name=\"Activity1\" keys=\"concept:name\"/>\n")

        # some other stuff
        xes_file.write("\t" + "<string key=\"lifecycle:model\" value=\"standard\"/>\n")

        def make_row(attr_type, key, value):
            return "<{0} key=\"{1}\" value=\"{2}\"/>\n".format(attr_type, key, value)

        def write_event(content, tab):
            xes_file.write(tab + "<event>\n")
            tab += "\t"
            for row in content:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            tab = tab[:-1]
            xes_file.write(tab + "</event>\n")

        def write_trace(properties, events, tab="\t"):
            xes_file.write(tab + "<trace>\n")
            tab += "\t"
            for row in properties:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            for event in events:
                write_event(event, tab)
            tab = tab[:-1]
            xes_file.write(tab + "</trace>\n")

        # NB: data in csv file must be in format "step_no_old", "step_no", "action", "step_type", "quiz_type", "time:timestamp", "student_id"
        # ORDERED BY user_id, timestamp
        # timestamp example: "2014-10-25T17:00:27.000+03:00"
        with open(source_file_name, 'r') as csv_file:
            cur_user_id = -1
            trace_properties = []
            trace_events = []
            for line in csv_file:
                line = line[:-1]        # end of line character
                # user_id, step_no, step_type, action, timestamp = line.split(',')
                old_step_no, new_step_no, action, step_type, quiz_type, timestamp, user_id = line.split(',')
                # print("s" + step_type)
                if cur_user_id != user_id:
                    # new user !
                    # ??? do we need events "Start\\Start" and "End\\End"
                    if cur_user_id != -1:
                        write_trace(trace_properties, trace_events)
                    trace_properties = [["string", "concept:name", user_id]]
                    trace_events = []
                    cur_user_id = user_id

                new_event = []

                if with_actions:
                    new_event.append(["string", "concept:name", step_type + ":" + quiz_type + "_" + action])
                else:
                    new_event.append(["string", "concept:name", step_type + ":" + quiz_type])

                new_event.append(["date", "time:timestamp", timestamp])

                #new_event.append(["string", "step_no", step_no])
                #new_event.append(["string", "action", action])
                #new_event.append(["string", "step_type", step_type])
                #new_event.append(["string", "quiz_type", quiz_type])
                trace_events.append(new_event)
            write_trace(trace_properties, trace_events)

        xes_file.write("</log>\n")


def make_xes_student_type(source_file_name, result_file_name, with_actions = False):
    # result_file_name = "01.xes"
    with open(result_file_name, 'w') as xes_file:
        xes_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xes_file.write("<log xes.version=\"1.0\" xmlns=\"http://www.xes-standard.org\" xes.creator=\"LENA\">\n")

        # EXTENSIONS
        xes_file.write("\t<extension name=\"Concept\" prefix=\"concept\" uri=\"http://www.xes-standard.org/concept.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Lifecycle\" prefix=\"lifecycle\" uri=\"http://www.xes-standard.org/lifecycle.xesext\"/>\n")
        xes_file.write("\t<extension name=\"Time\" prefix=\"time\" uri=\"http://www.xes-standard.org/time.xesext\"/>\n")

        # GLOBALS
        # trace has to have "concept:name" attribute
        xes_file.write("\t" + "<global scope=\"trace\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t"
                          "</global>\n")
        # event has to have "concept:name", "time:timestamp", "step_no", "action" and "step_type" attributes
        # columns = ["step_no_old", "step_no", "action", "step_type", "quiz_type", "time:timestamp", "student_id"]
        xes_file.write("\t" + "<global scope=\"event\">\n\t\t"
                              "<string key=\"concept:name\" value=\"name\"/>\n\t\t"
                              "<date key=\"time:timestamp\" value=\"201-01-24T15:53:11.668+02:00\"/>\n\t\t"
                              #"<string key=\"step_no\" value=\"string\"/>\n\t\t"
                              #"<string key=\"action\" value=\"string\"/>\n\t\t"
                              #"<string key=\"quiz_type\" value=\"string\"/>\n\t"
                          "</global>\n")

        # CLASSIFIERS
        xes_file.write("\t" + "<classifier name=\"Activity1\" keys=\"concept:name\"/>\n")

        # some other stuff
        xes_file.write("\t" + "<string key=\"lifecycle:model\" value=\"standard\"/>\n")

        def make_row(attr_type, key, value):
            return "<{0} key=\"{1}\" value=\"{2}\"/>\n".format(attr_type, key, value)

        def write_event(content, tab):
            xes_file.write(tab + "<event>\n")
            tab += "\t"
            for row in content:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            tab = tab[:-1]
            xes_file.write(tab + "</event>\n")

        def write_trace(properties, events, tab="\t"):
            xes_file.write(tab + "<trace>\n")
            tab += "\t"
            for row in properties:
                attr_type, key, value = row
                xes_file.write(tab + make_row(attr_type, key, value))
            for event in events:
                write_event(event, tab)
            tab = tab[:-1]
            xes_file.write(tab + "</trace>\n")

        # NB: data in csv file must be in format "step_no_old", "step_no", "action", "step_type", "quiz_type", "time:timestamp", "student_id"
        # ORDERED BY user_id, timestamp
        # timestamp example: "2014-10-25T17:00:27.000+03:00"
        with open(source_file_name, 'r') as csv_file:
            cur_user_id = -1
            trace_properties = []
            trace_events = []
            for line in csv_file:
                line = line[:-1]        # end of line character
                # user_id, step_no, step_type, action, timestamp = line.split(',')
                old_step_no, new_step_no, action, step_type, quiz_type, timestamp, user_id = line.split(',')
                # print("s" + step_type)
                if cur_user_id != user_id:
                    # new user !
                    # ??? do we need events "Start\\Start" and "End\\End"
                    if cur_user_id != -1:
                        write_trace(trace_properties, trace_events)
                    trace_properties = [["string", "concept:name", user_id]]
                    trace_events = []
                    cur_user_id = user_id

                new_event = []

                if with_actions:
                    new_event.append(["string", "concept:name", step_type + ":" + quiz_type + "_" + action])
                else:
                    new_event.append(["string", "concept:name", step_type + ":" + quiz_type])

                new_event.append(["date", "time:timestamp", timestamp])

                #new_event.append(["string", "step_no", step_no])
                #new_event.append(["string", "action", action])
                #new_event.append(["string", "step_type", step_type])
                #new_event.append(["string", "quiz_type", quiz_type])
                trace_events.append(new_event)
            write_trace(trace_properties, trace_events)

        xes_file.write("</log>\n")


"""
# without actions:
source_file = "D:\stepic\data\\67_quiz_type.csv"
result_file = source_file.replace(".csv", ".xes")
make_xes_quiz_type_and_video(source_file, result_file)

source_file = "D:\stepic\data\\70_quiz_type.csv"
result_file = source_file.replace(".csv", ".xes")
make_xes_quiz_type_and_video(source_file, result_file)
"""

"""
# with actions:
source_file = "D:\stepic\data\\67_quiz_type.csv"
result_file = source_file.replace(".csv", "_actions.xes")
make_xes_quiz_type_and_video(source_file, result_file, with_actions=True)

source_file = "D:\stepic\data\\70_quiz_type.csv"
result_file = source_file.replace(".csv", "_actions.xes")
make_xes_quiz_type_and_video(source_file, result_file, with_actions=True)
"""


