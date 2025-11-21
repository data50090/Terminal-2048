import curses;
SQUARE_SIZE = 10;

def drw(wd,x,y,num):
    wd.addch(y,x,curses.ACS_ULCORNER);
    wd.addch(y,x+(SQUARE_SIZE-1),curses.ACS_URCORNER);
    wd.addch(y+(SQUARE_SIZE // 2 - 1),x,curses.ACS_LLCORNER);
    wd.addch(y+(SQUARE_SIZE // 2 - 1),x+(SQUARE_SIZE-1),curses.ACS_LRCORNER);
    wd.hline(y,x+1,curses.ACS_HLINE,(SQUARE_SIZE - 2));
    wd.hline(y+(SQUARE_SIZE//2 - 1),x+1,curses.ACS_HLINE,(SQUARE_SIZE - 2));
    wd.vline(y+1,x,curses.ACS_VLINE,(SQUARE_SIZE//2 - 2));
    wd.vline(y+1,x + (SQUARE_SIZE-1),curses.ACS_VLINE,(SQUARE_SIZE//2 - 2));
    st = str(num);
    if (len(str(num))%2):
        st = "0" + st;
    wd.addstr(y+((SQUARE_SIZE//2) // 2),x + (SQUARE_SIZE//2-1) - ((len(str(num)) - 1)//2),st);

board = [ [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0] ];

id = [ [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0] ];
avail = [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1];

def init(scr):
    #variables
    ext = False;
    tr_time = 20; #in ms
    mainscr = True;
    #init
    curses.noecho();
    curses.cbreak();
    curses.curs_set(0);
    scr.keypad(True);
    scr.addstr(0,0,"2048 TERMINAL");
    scr.refresh();
    mainwin = curses.newwin(30,60,1,0);
    stats = curses.newwin(30,12,1,60);
    inp = curses.newwin(5,72,31,0);
    mainwin.box(curses.ACS_VLINE,curses.ACS_HLINE);
    stats.box(curses.ACS_VLINE,curses.ACS_HLINE);
    inp.box(curses.ACS_VLINE,curses.ACS_HLINE);
    drw(mainwin,5,5,25);
    mainwin.refresh();
    stats.refresh();
    inp.refresh();
    while (not ext):
          pass; 
    curses.echo();
    curses.nocbreak();
    scr.keypad(False);
    quit();



curses.wrapper(init);