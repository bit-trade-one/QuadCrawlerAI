# クアッドクローラーAIでROSに対応する方法                                                        
  
## 動作環境  
  
以下環境で確認しています  
 - ubuntu 18.04 LTS  
 - ROS melodic  
 - python 2.7.17  
（Win10のWSLで実現したROS環境でも実行可能ですが、ポートフォワーディングやファイアーウォールの設定等が必要です）  
  
## ROS対応の概要  
  
クアッドクローラーAIのプログラムはWebsocket通信でWebブラウザーから制御する構成になっています。  
ROSで制御をするには　「ROSトピックの内容をWebsocketに変換してクアッドクローラーAIに送信する」  
  
という動作をする中間プログラムを製作します。  
プログラミング言語はPythonです。websocketを使用するためにライブラリのインストールが必要です。  
  
## 準備  
  
Pythonのwebsocketライブラリのインストール  
  
```  
$ sudo pip install websocket-client  
```  
  
以下のテストプログラムを修正して、Websocketを使用した通信確認をします  
qctest01.py  
  
13行目にて、クアッドクローラーAIに設定されたipアドレスを設定します  
  
```  
ws = create_connection("ws://「クアッドクローラーAIのIPアドレス」:54323")  
```  
  
設定例（IPアドレスが　192.168.1.136の場合）  
  
```  
ws = create_connection("ws://192.168.1.136:54323")  
```  
  
クアッドクローラーのSSID・パスワード・IPアドレス　の設定は事前につくるっちで行ってください。  
IPアドレスを確認する手段としては、クアッドクローラーをPCとUSBケーブルで接続して、テラターム等で接続先のSSIDやIPアドレスが確認出来ます。  
(各PCでUSB接続時に構成されたCOMポートにて115200bpsで接続してください）  
  
IPアドレスを修正しましたらプログラムを実行してください  
  
```  
$ python qctest01.py  
```  
  
正常に実行できた場合、クアッドクローラーAIは　フルカラーLEDの点灯、ブザーの発音、前進・ポーズ等の動作　を行います。  
うまくクアッドクローラーAIに接続できない場合は、Pythonプログラム実行前にクアッドクローラーAIのリセットスイッチを押してみてください。  
  
このプログラムの内容だけでも理解できると、PythonプログラムでクアッドクローラーAIを遠隔制御する事が可能になります。  
  
## ROS対応プログラム  
  
### cmd_velでクアッドクローラーを制御するプログラム  
  
cmd_velをサブクスライブしてwebsocktに変換してクアッドクローラーに送信するプログラムです。  
  
ｘリニア方向（前進後進）、Yリニア方向（左右カニ歩き）、Z軸回転（超信地旋回）に対応します  
  
速度の値については絶対値ではなく５段階の動作速度に割り振っています。  
  
動作確認においてはcmd_velを手動でパブリッシュするのは面倒なので、キーボードでcmd_velの操作が行える　teleop-twist-keyboard を使用します。  
  
teleop-twist-keyboard　のインストールは  
ROS kineticなら  
  
```  
$ sudo apt-get install ros-kinetic-teleop-twist-keyboard  
```  
  
ROS melodicなら  
  
```  
$ sudo apt-get install ros-melodic-teleop-twist-keyboard  
```  
  
以下のcmd_vel対応プログラムの9行目を修正して、クワッドクローラAIのIPアドレスを設定します。  
cmd_vel2qc01.py  
  
動作をさせます  
  
一つ目のコンソールにてteleop_twist_keyboardを実行します  
  
```  
$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py  
```  
  
もう一つのコンソールにてクアッドクローラーAIのcmd_vel対応プログラムを起動します  
  
```  
$ python cmd_vel2qc01.py  
```  
  
teleop_twist_keyboardを起動したコンソールをアクティブにして、キーボードの”i” ”,” ”j” ”l”キーでクアッドクローラーの操作が出来ます　（キー操作についてはコンソールにも説明が出ます）  
  
  
  
  
  
### PS3コントローラーでクアッドクローラーAIを制御するプログラム  
  
Joy_nodeを使用する事で、PS2コントローラーでクアッドクローラーAIの制御が可能になります。  
左側のアナログコントロールレバーでクアッドクローラーAIの前後移動とCW/CCW回転の操作が行えます  
  
このプログラムを使用するには、事前にJoy_nodeをインストールしてください。  
  
ROS kineticの場合は  
  
```  
$ sudo apt-get install ros-kinetic-joy  
$ sudo apt-get install ros-kinetic-joystick-drivers  
```  
  
ROS melodicの場合は  
  
```  
$ sudo apt-get install ros-melodic-joy  
$ sudo apt-get install ros-melodic-joystick-drivers  
```  
  
  
  
以下のJoy_node対応プログラムの9行目にて、クワッドクローラAIのIPアドレスを設定します。  
cmd_vel2qc01.py  
  
プログラムの動作をさせます  
一つ目のコンソールにてJoy_nodeの起動  
  
```  
$ rosrun joy joy_node  
```  
  
もう一つのコンソールにてクアッドクローラーAIのJoy_node対応プログラムを起動します  
  
```  
$ python joy2qc01.py  
```  
  
左側のアナログコントローラーを前後に倒すと前後移動、左右に倒すとCW/CCWで超信地旋回します。  
  
アナログコントロールレバーの倒す角度で動作速度も変わります。  
  
動作確認したPS3コントローラーは汎用品を使用しています。またUSB接続時に操作ボタンの割付が変わる場合がありUSBの抜き差しで元にもどる場合もあります。  
もしボタン割り付けがおかしい場合は、ソースコードの155行からの4行でコントロールレバーの割付け（0～4）をしていますので入替をして下さい。  
  
    lx = joy_msg.axes[0]  
    ly = joy_msg.axes[1]  
    rx = joy_msg.axes[3]  
    ry = joy_msg.axes[4]
