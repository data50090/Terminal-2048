import curses
import random
SQUARE_SIZE = 10
TOPLEFT = [5,5]
TR_FRAME = 3
TR_TIME = 20 #in ms vvvv
POP_DELAY = 100
def drw(wd,x,y,num):
    wd.addch(y,x,curses.ACS_ULCORNER)
    wd.addch(y,x+(SQUARE_SIZE-1),curses.ACS_URCORNER)
    wd.addch(y+(SQUARE_SIZE // 2 - 1),x,curses.ACS_LLCORNER)
    wd.addch(y+(SQUARE_SIZE // 2 - 1),x+(SQUARE_SIZE-1),curses.ACS_LRCORNER)
    wd.hline(y,x+1,curses.ACS_HLINE,(SQUARE_SIZE - 2))
    wd.hline(y+(SQUARE_SIZE//2 - 1),x+1,curses.ACS_HLINE,(SQUARE_SIZE - 2))
    wd.vline(y+1,x,curses.ACS_VLINE,(SQUARE_SIZE//2 - 2))
    wd.vline(y+1,x + (SQUARE_SIZE-1),curses.ACS_VLINE,(SQUARE_SIZE//2 - 2))
    st = str(num)
    if (len(str(num))%2):
        st = "0" + st
    wd.addstr(y+((SQUARE_SIZE//2) // 2),x + (SQUARE_SIZE//2-1) - ((len(str(num)) - 1)//2),st)
def drwcord(wd,x,y,num):
    drw(wd,SQUARE_SIZE*x + TOPLEFT[0],(SQUARE_SIZE//2)*y + TOPLEFT[1],num)
def cvt(v,md):
    if (md):
        return (SQUARE_SIZE//2)*v + TOPLEFT[1]
    else:
        return SQUARE_SIZE*v + TOPLEFT[0]

board = [ [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0] ]
oboard = [ [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0] ]
# board[y][x] x = l to r, y = up to bt


# for funny animation bs (id and stuff)
remid = {}
idn = {}
id = [ [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0] ]

oid = [ [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0] ]
avail = [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]

def render(wd):
    global oid
    global id
    global avail
    global board
    global oboard
    global remid
    global idn
    query = []
    qrem = []
    oidn = []
    qr = []
    wd.clear()
    idn.clear()
    for i in range(0,4):
        s = ""
        for j in range(0,4):
            s += str(id[i][j])
            if (id[i][j]):
                idn[id[i][j]] = [i,j]
        print(s)
    print("\n")
    for i in range(0,4):
        for j in range(0,4):
            if (oid[i][j]):
                oidn.append(oid[i][j])
                if (oid[i][j] in idn):
                    query.append([[i,j],idn[oid[i][j]]])
                else:
                    qrem.append([ [i,j] , idn[remid[oid[i][j]]] ])
    
    for fr in range(0,TR_FRAME):
        wd.clear()
        if (fr != TR_FRAME-1):
            for a in qrem:
                dx = cvt(a[1][1],0) - cvt(a[0][1],0)
                dy = cvt(a[1][0],1) - cvt(a[0][0],1)
                print(dx,dy)
                dx = dx//TR_FRAME
                dy = dy//TR_FRAME
                
                drw(wd,cvt(a[0][1],0) + dx*(fr+1) , cvt(a[0][0],1) + dy*(fr+1),oboard[a[0][0]][a[0][1]])
            for a in query:
                dx = cvt(a[1][1],0) - cvt(a[0][1],0)
                dy = cvt(a[1][0],1) - cvt(a[0][0],1)
                dx = dx//TR_FRAME
                dy = dy//TR_FRAME
                drw(wd,cvt(a[0][1],0) + dx*(fr+1) , cvt(a[0][0],1) + dy*(fr+1),oboard[a[0][0]][a[0][1]])
        else:
            for i in range(0,4):
                for j in range(0,4):
                    if (board[i][j]):
                        if (id[i][j] in oidn):
                            drwcord(wd,j, i,board[i][j])
                        else:
                            qr.append([i,j])
        wd.refresh()
        curses.napms(TR_TIME)
    
    curses.napms(POP_DELAY)
    for a in qr:
         drwcord(wd,a[1],a[0],board[a[0]][a[1]])
    wd.refresh()



def compute(dirx,diry):
    global id
    global avail
    global board
    for i in range(0,4):
        for _ in range(0,4):
            for j in range(0,4):
                dir = dirx
                x = abs((dir>0)*3 - j)
                y = i
                if (diry != 0):
                    dir = diry
                    x = i
                    y = abs((dir>0)*3 - j)
                if (not (y-diry < 0 or y-diry >= 4 or x-dirx < 0 or x-dirx >= 4) ):
                    if (board[y][x] == 0):
                        board[y][x] = board[y-diry][x-dirx]
                        board[y-diry][x-dirx] = 0
                        id[y][x] = id[y-diry][x-dirx]
                        id[y-diry][x-dirx] = 0

def combine(dirx,diry):
    global id
    global avail
    global board
    global remid
    for i in range(0,4):
        for j in range(0,4):
            dir = dirx
            x = abs((dir>0)*3 - j)
            y = i
            if (diry != 0):
                dir = diry
                x = i
                y = abs((dir>0)*3 - j)
            if (not (y-diry < 0 or y-diry >= 4 or x-dirx < 0 or x-dirx >= 4) ):
                if (board[y][x] == board[y-diry][x-dirx] and board[y][x] != 0):
                    avail.append(id[y][x])
                    remid[id[y][x]] = id[y-diry][x-dirx]
                    id[y][x] = id[y-diry][x-dirx]
                    id[y-diry][x-dirx] = 0
                    board[y][x] = 2*board[y][x]
                    board[y-diry][x-dirx] = 0

UPKEY = [ord("w"),curses.KEY_UP]
RIGHTKEY = [ord("d"),curses.KEY_RIGHT]
DOWNKEY = [ord("s"),curses.KEY_DOWN]
LEFTKEY = [ord("a"),curses.KEY_LEFT]
def move(dirx,diry):
    compute(dirx,diry)
    combine(dirx,diry)
    compute(dirx,diry)


def game(scr,wd):
    global id
    global avail
    global board
    global oid
    global oboard
    for i in range(0,4):
        for j in range(0,4):
            board[i][j] = 0
            id[i][j] = 0
    for _ in range(0,2):
        while True:
            x = random.randrange(0,4)
            y = random.randrange(0,4)
            four = random.randrange(0,10)
            val = 2
            if (not four):
                val = 4
            if (board[x][y] > 0):
                continue
            board[x][y] = val
            id[x][y] = avail.pop()
            break
    #game logic
    render(wd)
    cnt = 14
    while True:
        if (cnt == 0):
            prevb = board
            combine(0,1)
            combine(0,-1)
            combine(1,0)
            combine(-1,0)
            if (prevb == board):
                break
            board = prevb
        nextid = avail.pop()
        for i in range(0,4):
            for j in range(0,4):
                oid[i][j] = id[i][j]
                oboard[i][j] = board[i][j]
        keyp = scr.getch()
        if (keyp in UPKEY):
            move(0,-1)
        if (keyp in RIGHTKEY):
            move(1,0)
        if (keyp in DOWNKEY):
            move(0,1)
        if (keyp in LEFTKEY):
            move(-1,0)
        if (board == oboard):
            avail.append(nextid)
            continue
        avb = []
        cnt = 0
        for i in range(0,4):
            for j in range(0,4):
                if (board[i][j] == 0):
                    avb.append([i,j])
                    cnt += 1
        if (cnt == 0):
            avail.append(nextid)
            continue
        rng = random.randrange(0,cnt)
        val = 2 + (random.randrange(0,10) == 0)*2
        board[avb[rng][0]][avb[rng][1]] = val
        id[avb[rng][0]][avb[rng][1]] = nextid
        print(f"next avail: {nextid}")
        cnt += 1
        render(wd)
    
        

def init(scr):
    global idprev
    global id
    global avail
    global board
    #variables
    ext = False
    mainscr = True
    #init
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    scr.keypad(True)
    scr.addstr(0,0,"2048 TERMINAL")
    scr.refresh()
    mainwin = curses.newwin(30,60,1,0)
    stats = curses.newwin(30,12,1,60)
    inp = curses.newwin(5,72,31,0)
    mainwin.box(curses.ACS_VLINE,curses.ACS_HLINE)
    stats.box(curses.ACS_VLINE,curses.ACS_HLINE)
    inp.box(curses.ACS_VLINE,curses.ACS_HLINE)
    mainwin.refresh()
    stats.refresh()
    inp.refresh()
    game(scr,mainwin)
    curses.echo()
    curses.nocbreak()
    scr.keypad(False)
    quit()



curses.wrapper(init)