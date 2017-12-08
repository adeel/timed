# timed

[Timed](http://github.com/adeel/timed) is a command-line time tracker.

## Summary

    $ timed start myproject
    starting work on myproject
      at 16:35 on 07 Feb 2011

    $ timed
    working on myproject:
      from     16:35 on 07 Feb 2011
      to now,  17:00 on 07 Feb 2011
            => 0h25m have elapsed

    $ timed stop
    worked on myproject
      from    16:35 on 07 Feb 2011
      to now, 17:40 on 07 Feb 2011
           => 1h5m elapsed

    $ timed summary
    myproject   1h5m

    $ cat ~/.timed
    myproject: 16:35 on 07 Feb 2011 - 17:40 on 07 Feb 2011

    $ cat ~/.timed | grep "Jan 2011" | timed parse

## Installation

From GitHub:

      $ git clone git://github.com/adeel/timed.git
      $ cd timed
      # python setup.py install

From Pypi:

      # pip install timed

For Arch Linux, Tom Vincent (@tlvince) has prepared a [PKGBUILD](https://github.com/tlvince/pkgbuild/blob/master/python-timed/PKGBUILD).

## Usage

    timed: alias for 'timed status'

    timed status:
           print current status

    timed start <project>:
           start tracking for <project>

    timed stop:
           stop tracking for the active project

    timed summary:
           show a summary of all projects

    timed parse:
           parses a stream with text formatted as a Timed logfile and shows a
           summary

    timed help:
           print help

## Bonus

Enable tab completion for project names by putting this in your .bashrc:

    shopt -s progcomp                                                               
    timed_complete() {                                                              
      local partial                                                                 
      COMPREPLY=()                                                                  
      partial=${COMP_WORDS[COMP_CWORD]}                                             
      COMPREPLY=($(compgen -W '$( timed projects )' -- $partial))                   
      return 0                                                                      
    }                                           
    complete -F timed_complete -o dirnames timed

## Thanks

Thanks to [Tom Vincent](http://github.com/tlvince).

## License

Copyright (c) 2011 Adeel A. Khan <adeel@yusufzai.me>.

MIT license.
