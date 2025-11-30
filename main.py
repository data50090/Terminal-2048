import curses
import random

SQUARE_SIZE = 10
TOPLEFT = [9,3]
TR_FRAME = 3
TR_TIME = 20 #in ms vvvv
POP_DELAY = 30
SCORE = 0
WINSTATE = False
titleb = "nothing"
inp = "nothing"
def drw(wd,x,y,num):
    for i in range(y,y+(SQUARE_SIZE // 2)):
        wd.addstr(i,x," "*SQUARE_SIZE)
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
    wd.addstr(y+((SQUARE_SIZE//2) // 2),x + (SQUARE_SIZE//2-1) - ((len(str(num)) - 1)//2),st,curses.color_pair(0))


asciiart = """     
██████   
     ██  
 █████   
██       
███████  
         
         
 █████  
██   ██ 
██   ██ 
██   ██ 
 █████  
         
         
██   ██  
██   ██  
███████  
     ██  
     ██  
         
         
 █████   
██   ██  
 █████   
██   ██  
 █████   
         """
def rst():
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)

def rs():
    curses.resize_term(0, 0)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    if (curses.LINES < 37 or curses.COLS < 78):
        print("Terminal window too small. Consider resizing the terminal window larger.")
        rst()
        exit()
    global titleb
    global inp
    titleb.attron(curses.color_pair(1))
    inp.attron(curses.color_pair(1))
    titleb.box(curses.ACS_VLINE,curses.ACS_HLINE)
    inp.box(curses.ACS_VLINE,curses.ACS_HLINE)
    inp.attroff(curses.color_pair(1))
    titleb.attroff(curses.color_pair(1))
    inp.addstr(1,3,"MOVE: WASD/ARROW_KEY   NEW_GAME: N   QUIT: B   CONFIRM: V   CANCEL: C")
    inp.addstr(3,31, "--KEYBINDS--")
    start_y = 1
    for s in asciiart.split("\n"):
        titleb.addstr(start_y,5,s)
        start_y += 1
    titleb.refresh()
    inp.refresh()
def drw2(wd,x,y,ns,cl = True):
    SQUARE_SIZE = ns
    if (cl):
        for i in range(y,y+(SQUARE_SIZE // 2)):
            wd.addstr(i,x," "*SQUARE_SIZE)
    wd.addch(y,x,curses.ACS_ULCORNER)
    wd.addch(y,x+(SQUARE_SIZE-1),curses.ACS_URCORNER)
    wd.addch(y+(SQUARE_SIZE // 2 - 1),x,curses.ACS_LLCORNER)
    wd.addch(y+(SQUARE_SIZE // 2 - 1),x+(SQUARE_SIZE-1),curses.ACS_LRCORNER)
    wd.hline(y,x+1,curses.ACS_HLINE,(SQUARE_SIZE - 2))
    wd.hline(y+(SQUARE_SIZE//2 - 1),x+1,curses.ACS_HLINE,(SQUARE_SIZE - 2))
    wd.vline(y+1,x,curses.ACS_VLINE,(SQUARE_SIZE//2 - 2))
    wd.vline(y+1,x + (SQUARE_SIZE-1),curses.ACS_VLINE,(SQUARE_SIZE//2 - 2))


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
    global SCORE
    query = []
    qrem = []
    oidn = []
    qr = []
    wd.clear()
    wd.box(curses.ACS_VLINE,curses.ACS_HLINE)
    drw2(wd,TOPLEFT[0]-2,TOPLEFT[1]-1,SQUARE_SIZE*4+4,False)
    wd.addstr(TOPLEFT[1]-2,TOPLEFT[0]-1,f"SCORE: {SCORE}")
    idn.clear()
    for i in range(0,4):
        s = ""
        for j in range(0,4):
            s += str(id[i][j])
            if (id[i][j]):
                idn[id[i][j]] = [i,j]
#        print(s)
#    print("\n")
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
        wd.box(curses.ACS_VLINE,curses.ACS_HLINE)
        drw2(wd,TOPLEFT[0]-2,TOPLEFT[1]-1,SQUARE_SIZE*4+4,False)
        wd.addstr(TOPLEFT[1]-2,TOPLEFT[0]-1,f"SCORE: {SCORE}")
        if (fr != TR_FRAME-1):
            for a in qrem:
                dx = cvt(a[1][1],0) - cvt(a[0][1],0)
                dy = cvt(a[1][0],1) - cvt(a[0][0],1)
#                print(dx,dy)
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
         t_size = SQUARE_SIZE-4
         drw2(wd,cvt(a[1],0)+2,cvt(a[0],1)+1,t_size)
         wd.refresh()
         curses.napms(POP_DELAY)
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
    global SCORE
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
                    SCORE += board[y][x]
                    board[y-diry][x-dirx] = 0

UPKEY = [ord("w"),curses.KEY_UP]
RIGHTKEY = [ord("d"),curses.KEY_RIGHT]
DOWNKEY = [ord("s"),curses.KEY_DOWN]
LEFTKEY = [ord("a"),curses.KEY_LEFT]
QUITKEY = ord("b")
NEWKEY = ord("n")
def move(dirx,diry):
    compute(dirx,diry)
    combine(dirx,diry)
    compute(dirx,diry)

def quitq(scr,wd):
    wd.addstr(25,14,"Are you sure you want to quit?")
    wd.addstr(26,17,"Confirm: V | Cancel: C")
    wd.refresh()
    while True:
        cm = scr.getch()
        if (cm == ord("v")):
            rst()
            exit()
        if (cm == ord("c")):
            wd.move(25,1)
            wd.clrtoeol()
            wd.move(26,1)
            wd.clrtoeol()
            wd.box(curses.ACS_VLINE,curses.ACS_HLINE)
            wd.refresh()
            return
def newq(scr,wd,bl):
    if (bl == 1):
        wd.addstr(25,25,"New Game?")
        wd.addstr(26,18,"Confirm: V | Cancel: C")
    else:
        if (bl == 0):
            wd.addstr(25,18,"Game Over. New Game?")
            wd.addstr(26,18,"Confirm: V | Quit: B")
        else:
            wd.addstr(25,17,"You Got 2048! New Game?")
            wd.addstr(26,13,"Confirm: V | Continue Playing: C")
    wd.refresh()
    while True:
        cm = scr.getch()
        if (cm == ord("v")):
            return True
        if (cm == ord("c") and bl > 0):
            wd.move(25,1)
            wd.clrtoeol()
            wd.move(26,1)
            wd.clrtoeol()
            wd.box(curses.ACS_VLINE,curses.ACS_HLINE)
            wd.refresh()
            return False
        if (cm == QUITKEY and not bl):
            rst()
            exit()

cnt = 0
def game(scr,wd):
    global id
    global avail
    global board
    global oid
    global oboard
    global cnt
    global SCORE
    global WINSTATE
    SCORE = 0
    WINSTATE = False
    for i in range(0,4):
        for j in range(0,4):
            board[i][j] = 0
            oboard[i][j] = 0
            id[i][j] = 0
            oid[i][j] = 0
            avail.clear()
            for k in range(1,21):
                avail.append(k)
            cnt = 14

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
    while True:
        nextid = avail.pop()
        for i in range(0,4):
            for j in range(0,4):
                oid[i][j] = id[i][j]
                oboard[i][j] = board[i][j]
                if (board[i][j] == 2048 and not WINSTATE):
                    WINSTATE = True
                    if (newq(scr,wd,2)):
                        return

        if (cnt == 0):
            move(0,1)
            move(0,-1)
            move(1,0)
            move(-1,0)
            if (board == oboard):
                newq(scr,wd,False)
                return
            for i in range(0,4):
                for j in range(0,4):
                    id[i][j] = oid[i][j]
                    board[i][j] = oboard[i][j]
        keyp = scr.getch()
        if (keyp == QUITKEY):
            quitq(scr,wd)
        if (keyp == NEWKEY):
            if (newq(scr,wd,True)):
                return
        if (keyp in UPKEY):
            move(0,-1)
        if (keyp in RIGHTKEY):
            move(1,0)
        if (keyp in DOWNKEY):
            move(0,1)
        if (keyp in LEFTKEY):
            move(-1,0)
        if (keyp == curses.KEY_RESIZE):
            rs()
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
#        print(f"next avail: {nextid}")
        cnt -= 1
        render(wd)

def init(scr):
    global id
    global avail
    global board
    global inp
    global titleb
    #init
    if (curses.LINES < 37 or curses.COLS < 78):
        print("Terminal window too small. Consider resizing the terminal window.")
        rst()
        exit()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    scr.keypad(True)
    curses.init_pair(1,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    scr.addstr(0,0,"2048 TERMINAL",curses.color_pair(1))
    scr.refresh()
    mainwin = curses.newwin(30,60,1,0)
    titleb = curses.newwin(30,17,1,60)
    inp = curses.newwin(5,77,31,0)
    mainwin.attron(curses.color_pair(1))
    mainwin.box(curses.ACS_VLINE,curses.ACS_HLINE)
    rs()
    mainwin.refresh()
    while True:
        game(scr,mainwin)


curses.wrapper(init)