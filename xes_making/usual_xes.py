def correct_timestamp(timestamp):
    # "2014-12-21 11:28:17" to
    # "2014-11-11T08:24:42.000+00:00"
    d, t = timestamp.split(' ')
    return "{0}T{1}.000+00:00".format(d, t)

def make_usual_xes(source_file_name, result_file_name):
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
                timestamp = correct_timestamp(timestamp)
                if cur_user_id != user_id:
                    # new user !
                    if cur_user_id != -1:
                        write_trace(trace_properties, trace_events)
                    trace_properties = [["string", "concept:name", user_id]]
                    trace_events = []
                    cur_user_id = user_id

                new_event = []

                # name of event:
                event_name = "{0}--{2} {1} ({3})".format(old_step_no, step_type, action, new_step_no)
                new_event.append(["string", "concept:name", event_name])

                new_event.append(["date", "time:timestamp", timestamp])

                #new_event.append(["string", "step_no", step_no])
                #new_event.append(["string", "action", action])
                #new_event.append(["string", "step_type", step_type])
                #new_event.append(["string", "quiz_type", quiz_type])
                trace_events.append(new_event)
            write_trace(trace_properties, trace_events)

        xes_file.write("</log>\n")


source_file = "D:\stepic\data\\67_logs.csv"
result_file = "D:\stepic\data\\usual xes\\67_usual.xes"
make_usual_xes(source_file, result_file)

source_file = "D:\stepic\data\\70_logs.csv"
result_file = "D:\stepic\data\\usual xes\\70_usual.xes"
make_usual_xes(source_file, result_file)