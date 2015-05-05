from __future__ import division
from collections import defaultdict
from itertools import groupby

import sys
sys.stdout = open('output.txt', 'w')


class Ref():
    def __init__(self, count, destination):
        self.count = int(count)
        self.dest = destination

    def __iter__(self):
        yield self.count
        yield self.dest


class RelRef():
    def __init__(self, source, destination, count, source_type="unknown", dest_type="unknown"):
        self.count = int(count)
        self.source_num = int(source)
        self.dest_num = int(destination)

        self.rel = self.dest_num - self.source_num

        self.source_type = source_type
        self.dest_type = dest_type


def read_links(filename):
    with open(filename, 'r') as fin:
        in_links, out_links = defaultdict(list), defaultdict(list)
        dest = None
        for line in fin:
            if dest is None:
                # заголовок: нужно понять, куда будут ссылки. первый символ заголовка -- запятая
                dest = line[1:].split(',')
                continue
            line = line.split(',')
            name, values = line[0], line[1:]
            if len(dest) != len(values):
                raise Exception("WRONG INPUT FORMAT")
            in_links[name] = [Ref(v, dest[i]) for i, v in enumerate(values) if int(v) > 0]
            for link in in_links[name]:
                c, who = link
                out_links[who].append(Ref(c, name))
    # сортировка
    for step in in_links:
        in_links[step] = sorted(in_links[step], reverse=True, key=lambda x: x.count)
    for step in out_links:
        out_links[step] = sorted(out_links[step], reverse=True, key=lambda x: x.count)

    return in_links, out_links


def filter(links, threshold=10):
    for step in links:
        links[step] = [r for r in links[step] if r.count > threshold]
    return links


def print_links(links):
    for step in links:
        print("links from (to) step {0}:".format(step))
        for reference in links[step]:
            print("\t{0} for {1} times".format(reference.dest, reference.count))

# читаем ссылки
in_links, out_links = read_links("D:\\stepic\\data\\metrics\\67_usual\\Relations - Absolute Frequency.csv")

# фильтруем редкие:
in_links, out_links = filter(in_links), filter(out_links)

step_id = {}
step_type = {}
for step in out_links:
    num = step.split('(')[-1].split(')')[0]
    if num not in step_id:
        cur_id = step.split('-')[0]
        step_id[num] = cur_id
        cur_type = step.split(' ')[1]
        step_type[num] = cur_type

# хотим преобразовать в относительные ссылки: на сколько степов вперед/назад ссылается
# сейчас работаем только с out_links
rel_links = {}
steps = sorted(list(out_links.keys()), key=lambda x: x.split('(')[-1].split(')')[0])
for step_num, actions in groupby(steps, key=lambda x: x.split('(')[-1].split(')')[0]):
    # теперь нужно просмотреть все исходящие ссылки из этого степа,
    # и посчитать переходы на другие степы
    counts = defaultdict(int)
    for link in [item for action in actions for item in out_links[action]]:
        counts[link.dest.split('(')[-1].split(')')[0]] += link.count
    rel_links[step_num] = [RelRef(step_num, dest_num, counts[dest_num], step_type[step_num], step_type[dest_num])
                           for dest_num in counts if step_num != dest_num]


# в rel_links относительные ссылки.
# посчитаем, насколько часто в среднем переходят теми или иными путями
step_num, quiz_num, video_num = len(step_type), \
                                len([s for s in step_type.values() if s == "quiz"]), \
                                len([s for s in step_type.values() if s == "video"])

frequencies = defaultdict(float)
type_freq = {"video": defaultdict(float), "quiz": defaultdict(float)}
for step in rel_links:
    links = rel_links[step]     # [r for r in rel_links[step] if r.count > 50]
    summ = sum([r.count for r in links])

    for r in links:
        frequencies[r.rel] += r.count / summ / step_num
        type_freq[r.dest_type][r.rel] += r.count / summ / (quiz_num if r.dest_type == "quiz" else video_num)

# выводим только результаты с частотой более одного процента
percent_threshold = 1
print("ALL REFERENCES")
for rel in [s for s in sorted(frequencies.keys(), key=lambda x: frequencies[x], reverse=True)
            if frequencies[s] * 100 > percent_threshold]:
    print("relative link to {0} happens in {1:.3f}% cases".format(rel, frequencies[rel] * 100))

print("\nREFERENCES TO QUIZES")
for rel in [s for s in sorted(type_freq["quiz"].keys(), key=lambda x: type_freq["quiz"][x], reverse=True)
            if frequencies[s] * 100 > percent_threshold]:
    print("relative link to {0} happens in {1:.3f}% cases".format(rel, type_freq["quiz"][rel] * 100) +
          "  ({0:.3f}% of all)".format(frequencies[rel] * 100 / step_num * quiz_num))

print("\nREFERENCES TO VIDEOS")
for rel in [s for s in sorted(type_freq["video"].keys(), key=lambda x: type_freq["video"][x], reverse=True)
            if frequencies[s] * 100 > percent_threshold]:
    print("relative link to {0} happens in {1:.3f}% cases".format(rel, type_freq["video"][rel] * 100) +
          "  ({0:.3f}% of all)".format(frequencies[rel] * 100 / step_num * video_num))


# посчитаем аналогичные частоты для конкретных степов (lesson #2232 и пара соседних степов)
some_steps = [str(i) for i in range(40, 50)]
for some_step in some_steps:
    some_step_freq = defaultdict(float)
    some_step_type_freq = {"video": defaultdict(float), "quiz": defaultdict(float)}
    links = rel_links[some_step]
    summ = sum([r.count for r in links])
    for r in links:
        some_step_freq[r.rel] += r.count / summ
        some_step_type_freq[r.dest_type][r.rel] += r.count / summ
    print("\n\nREFERENCES FOR STEP #{0} (id: {1}, type: {2})".format(some_step, step_id[some_step], step_type[some_step]))
    for rel in [s for s in sorted(some_step_freq.keys(), key=lambda x: some_step_freq[x], reverse=True)
                if some_step_freq[s] * 100 > percent_threshold]:
        print("relative link to {0} happens in {1:.3f}% cases".format(rel, some_step_freq[rel] * 100))