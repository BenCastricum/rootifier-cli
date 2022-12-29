#!/usr/bin/env python3

import re
import sys

def rm_insignificant_lines(in_stream):
    """
    Remove insignificant lines from input config file.
    These lines are starting with '#' or 'echo'
    :param in_cfg: cfg as a stream
    :return: cleanified array of config lines
    """
    cfg_arr = []
    for line in in_stream:
        if is_cfg_statement(line):
            cfg_arr.append(line)
    return cfg_arr


def is_cfg_statement(line):
    # if line is empty, or first for elemets are not spaces
    # consider this line for deletion
    if line.strip() == '' or line[0:4] != '    ':
        return False
    else:
        return True

def rootify(config):
    cfg_string = ['/configure']
    rootified_cfg = []
    # init previous indent level as 0 for /configure line
    prev_ind_level = 0

    for i, line in enumerate(config):

        if line.strip() == 'exit':
            cfg_string.pop()
            prev_ind_level -= 4
            continue

        # calc current indent
        cur_ind_level = len(line) - len(line.lstrip())

        # handle some special cases when appending config statements
        if cur_ind_level > prev_ind_level:

            if (re.search('\screate$', cfg_string[-1])):
                # create statements need to be printed out in any case
                rootified_cfg.append(' '.join(cfg_string))

                # strip the create part to continue
                cfg_string[-1] = re.sub('\screate$', '', cfg_string[-1])

                # some resources can be named upon creation, strip that too
                cfg_string[-1] = re.sub('\sname\s\".*\"', '', cfg_string[-1])

            # "Base" in "router Base" does not comply with the rest of the flow
            cfg_string[-1] = re.sub('router\sBase', 'router', cfg_string[-1])

        # if a command is on the same level of indent we delete the prev. command
        elif cur_ind_level == prev_ind_level:
            cfg_string.pop()
 
        cfg_string.append(line.strip())

        prev_ind_level = cur_ind_level

        # if we have a next line go check it's indent value
        if i < len(config) - 1:
            next_ind_level = len(config[i + 1]) - len(config[i + 1].lstrip())
            # if a next ind level is deeper (>) then we can continue accumulation
            # of the commands
            if next_ind_level > prev_ind_level:
                continue
            # if the next level is the same or lower, we must save a line
            else:
                rootified_cfg.append(' '.join(cfg_string))
        else:
            # otherwise we have a last line here, so print it
            rootified_cfg.append(' '.join(cfg_string))

    return rootified_cfg


if __name__ == '__main__':

    # use stdin if it's full                                                        
    if not sys.stdin.isatty():
        input_stream = sys.stdin
    # otherwise, read the given filename                                            
    else:
        try:
            input_filename = sys.argv[1]
        except IndexError:
            message = 'need filename as first argument if stdin is not full'
            raise IndexError(message)
        else:
            input_stream = open(input_filename, 'r')

    # we need to clean the config first otherwise the indent flow would be
    # disrupted with undesirable results.
    clean_cfg = rm_insignificant_lines(input_stream)
    print("\n".join(rootify(clean_cfg)))
