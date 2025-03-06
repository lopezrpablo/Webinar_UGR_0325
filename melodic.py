from music21 import *
from os import listdir
from collections import Counter
from statistics import median
from itertools import product, chain
import sys
import os
import time
import operator

    
def ambito(s):
    amb = analysis.discrete.Ambitus(s)
    amb = amb.getPitchSpan(s)
    result = amb[0].nameWithOctave + ' - ' + amb[1].nameWithOctave
    return result

def rec_notas(s, finalis):

    snotes = sorted([x.nameWithOctave for x in s.recurse().getElementsByClass('Note')])
    notes_ordered = list()
    tmp = list()
    cond = False

    for i in snotes:
        if cond is False:
            if i == finalis:
                cond = True
                notes_ordered.append(i)
            else:
                tmp.append(i)
        else:
            notes_ordered.append(i)

    if len(tmp) > 0:
        notes_ordered = notes_ordered + tmp
    else:
        pass


    nt_dict = Counter(notes_ordered)

    return nt_dict


def note_rest_ratio(s):
    nt_counter = 0
    rst_counter = 0

    for i in s.recurse().getElementsByClass(['Note', 'Rest']):
        
        if isinstance(i, note.Note):
            nt_counter += i.quarterLength
        else:
            rst_counter += i.quarterLength 
        
    return nt_counter/rst_counter


def armadura(s):
    alt = [i.name for i in s[key.KeySignature].first().alteredPitches]
    return alt

def get_counter_stats(dic, mode):

    if mode == 'notes':
        midi_notes_dirty = [[note.Note(k).pitch.midi] * v for k, v in dic.items()]
        midi_notes = [i for i in list(chain.from_iterable(midi_notes_dirty))]
        midi_notes.sort()
        median_note_midi = median(midi_notes)
        median_note = note.Note(median_note_midi).nameWithOctave

        highest = list(dic.most_common()[0])
        lowest = list(dic.most_common()[-1])
        highest_def = list()
        lowest_def = list()
        
        for k,v in dic.items():

            if v == highest[1]:
                highest_def.append(note.Note(k).pitch.midi)

            if v == lowest[1]:
                lowest_def.append(note.Note(k).pitch.midi)

        closeness_highest = None
        current_note_highest = None

        for i in highest_def:
            if closeness_highest is None:
                closeness_highest = abs(i - median_note_midi)
                current_note_highest = i

            else:
                if closeness_highest > abs(i - median_note_midi):
                    if abs(i - median_note_midi) == 0:
                        continue
                    else:
                        closeness_highest = abs(i - median_note_midi)
                        current_note_highest = i

        closeness_lowest = None
        current_note_lowest = None

        for i in lowest_def:
            if closeness_lowest is None:
                closeness_highest = abs(i - median_note_midi)
                current_note_lowest = i

            else:
                if closeness_lowest < abs(i - median_note_midi):
                    if abs(i - median_note_midi) == 0:
                        continue
                    else:
                        closeness_lowest = abs(i - median_note_midi)
                        current_note_lowest = i

        return note.Note(current_note_highest).nameWithOctave, median_note, note.Note(current_note_lowest).nameWithOctave

    elif mode == 'intervals':
        intervals_dirty = [[int(k)] * v for k, v in dic.items()]
        intervals_sorted = [i for i in list(chain.from_iterable(intervals_dirty))]
        intervals_sorted.sort()
        median_interval = median(intervals_sorted)

        highest = list(dic.most_common()[0])
        lowest = list(dic.most_common()[-1])
        highest_def = list()
        lowest_def = list()
        
        for k,v in dic.items():

            if v == highest[1]:
                highest_def.append(int(k))

            if v == lowest[1]:
                lowest_def.append(int(k))

        closeness_highest = None
        current_note_highest = None

        for i in highest_def:
            if closeness_highest is None:
                closeness_highest = abs(i - median_interval)
                current_note_highest = i

            else:
                if closeness_highest > abs(i - median_interval):
                    if abs(i - median_interval) == 0:
                        continue
                    else:
                        closeness_highest = abs(i - median_interval)
                        current_note_highest = i

        closeness_lowest = None
        current_note_lowest = None

        for i in lowest_def:
            if closeness_lowest is None:
                closeness_highest = abs(i - median_interval)
                current_note_lowest = i

            else:
                if closeness_lowest < abs(i - median_interval):
                    if abs(i - median_interval) == 0:
                        continue
                    else:
                        closeness_lowest = abs(i - median_interval)
                        current_note_lowest = i

        return str(current_note_highest), str(median_interval), str(current_note_lowest)

    else:
        
        durations = [[k] * v for k, v in dic.items()]
        durations_cleaned = [i for i in list(chain.from_iterable(durations))]
        durations_cleaned.sort()
        median_duration = median(durations_cleaned)

        highest = list(dic.most_common()[0])
        lowest = list(dic.most_common()[-1])
        highest_def = list()
        lowest_def = list()
        
        for k,v in dic.items():

            if v == highest[1]:
                highest_def.append(k)

            if v == lowest[1]:
                lowest_def.append(k)

        closeness_highest = None
        current_note_highest = None

        if len(highest_def) == 1:
            current_note_highest = highest_def[0]
        else:
            for i in highest_def:
                if closeness_highest is None:
                    closeness_highest = abs(i - median_duration)
                    current_note_highest = i

                else:
                    if closeness_highest > abs(i - median_duration):
                        if abs(i - median_duration) == 0:
                            continue
                        else:
                            closeness_highest = abs(i - median_duration)
                            current_note_highest = i

        closeness_lowest = None
        current_note_lowest = None

        if len(lowest_def) == 1:
            current_note_lowest = lowest_def[0]
        else:
            for i in lowest_def:
                if closeness_lowest is None:
                    closeness_highest = abs(i - median_duration)
                    current_note_lowest = i

                else:
                    if closeness_lowest < abs(i - median_duration):
                        if abs(i - median_duration) == 0:
                            continue
                        else:
                            closeness_lowest = abs(i - median_duration)
                            current_note_lowest = i

        return current_note_highest, median_duration, current_note_lowest

def get_dict_stats(dic):
    rest_value = dic['R']
    dic.pop('R')
    items = [(note.Note(k).pitch.midi, v) for k, v in dic.items()]
    items.sort(key=operator.itemgetter(1))
    items_cleaned = [i[0] for i in items]
    median_item = median(items_cleaned)
    
    highest = max(dic.values())
    lowest = min(dic.values())
    highest_def = list()
    lowest_def = list()
    
    dic['R'] = rest_value

    for k,v in dic.items():

        if v == highest:
            highest_def.append(note.Note(k).pitch.midi)

        if v == lowest:
            lowest_def.append(note.Note(k).pitch.midi)

    closeness_highest = None
    current_note_highest = None

    if len(highest_def) == 1:
        current_note_highest = highest_def[0]
    else:
        for i in highest_def:
            if closeness_highest is None:
                closeness_highest = abs(i - median_item)
                current_note_highest = i

            else:
                if closeness_highest > abs(i - median_item):
                    if abs(i - median_item) == 0:
                        continue
                    else:
                        closeness_highest = abs(i - median_item)
                        current_note_highest = i

    closeness_lowest = None
    current_note_lowest = None

    if len(lowest_def) == 1:
        current_note_lowest = lowest_def[0]
    else:
        for i in lowest_def:
            if closeness_lowest is None:
                closeness_highest = abs(i - median_item)
                current_note_lowest = i

            else:
                if closeness_lowest < abs(i - median_item):
                    if abs(i - median_item) == 0:
                        continue
                    else:
                        closeness_lowest = abs(i - median_item)
                        current_note_lowest = i

    return note.Note(current_note_highest).nameWithOctave, note.Note(median_item).nameWithOctave, note.Note(current_note_lowest).nameWithOctave