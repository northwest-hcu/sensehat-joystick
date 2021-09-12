#coding:utf-8
from sense_hat import SenseHat
import time

class joystickAction:
    #コンストラクタ
    def __init__(self):
        self.Obj=SenseHat() #SenseHatオブジェクト
        self.preTime=time.time() #前回イベントの時刻
        self.nowTime=time.time() #現在時刻
        self.lastAct=0 #前回イベントの動作
        self.lastDir=0 #前回イベントの方向
        self.funcArray=[] #イベントハンドラ情報のリスト
        
    #デストラクタ
    def __del__(self):
        print("") #改行を出力
    
    #要素１:actionを数値で返す(pressed:1, held:2, released:3, no action:0)
    #要素２:directionを数値で返す(左:1, 上:2, 右:3, 下:4, 中央:5, なし:0)
    #要素３:前のアクションからの時間を返す(継続時間の取得)
    def evAct(self):
        timeRange=time.time()-self.preTime
        
        for event in self.Obj.stick.get_events():
            if len(event)>0:
                self.nowTime=event.timestamp
                timeRange=self.nowTime-self.preTime

                #方向の情報
                if event.direction=="left":
                    dir=1
                elif event.direction=="up":
                    dir=2
                elif event.direction=="right":
                    dir=3
                elif event.direction=="down":
                    dir=4
                elif event.direction=="middle":
                    dir=5

                #現在の動作
                if event.action=="pressed":
                    action=1
                elif event.action=="held":
                    action=2
                elif event.action=="released":
                    action=3

                #動作が継続しているか
                if action!=self.lastAct:
                    self.preTime=event.timestamp

                #前の方向の更新
                if event.direction=="left":
                    self.lastDir=1
                elif event.direction=="up":
                    self.lastDir=2
                elif event.direction=="right":
                    self.lastDir=3
                elif event.direction=="down":
                    self.lastDir=4
                elif event.direction=="middle":
                    self.lastDir=5
                    
                #前の動作の更新
                if event.action=="pressed":
                    self.lastAct=1
                elif event.action=="held":
                    self.lastAct=2
                elif event.action=="released":
                    self.lastAct=3
                    
                return [action,dir,timeRange]
        #heldとno actionの判別
        if self.lastAct!=2:
            self.lastAct=0
            self.lastDir=0
        return [self.lastAct,self.lastDir,timeRange]

    #設定された関数の実行
    def evHandler(self):
        self.evHandler(self)

    #イベントハンドラの追加(設定する関数,対象動作,対象方向,関数判別キー)
    def evAdd(self,func,action,dir,key):
        handle=joystickAction()
        handle.evHandler=func
        self.funcArray.append((handle,action,dir,key))

    #イベントハンドラの削除(関数判別キー) ***設定した順で一番始めに関数判別キーが一致する関数を削除する
    def evRemove(self,key):
        for func in self.funcArray:
            if func[3]==key:
                self.funcArray.remove(func)
                break

    #イベントハンドラに設定された関数の実行
    def evFunc(self,action,dir):
        for event in self.funcArray:
            eventFunction=event[0]
            eventAction=event[1]
            eventDirection=event[2]
            if eventAction==action and eventDirection==dir:
                eventFunction.evHandler()
            
#-----ここから利用のサンプルコード-----

hat=joystickAction()

def func1():
    print("\nHello")
def func2():
    print("\nWorld")
    
hat.evAdd(func1,1,1,"f1")
hat.evAdd(func2,1,1,"f2")
hat.evAdd(func1,1,2,"f3")
hat.evRemove("f1")

try:
    while True:
        act=hat.evAct()
        hat.evFunc(act[0],act[1])
        print("time:"+str(act[2])+" s")
            

except KeyboardInterrupt:
    pass
