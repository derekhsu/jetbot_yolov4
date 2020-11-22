#### <span style="color:blue">Jetbot 開機設定</span>

基本上, 根據此篇文章操作 https://jetbot.org/master/index.html  
> 1. 下載及燒錄 image
>   - 我用的是 4GB 的版本
>   - 簡單判斷 2GB 或 4GB 的方式：看充電的接頭是 micro USB 的是 for Jetson Nano (4GB), 或是 USB-C (for Jetson Nano 2GB)   

|Platform	|JetPack Version	|JetBot Version	|Download|
|:------------- |:-------------|:-----|:-----|
|Jetson Nano (4GB)	|4.4.1	|0.4.2	|[jetbot-042_nano-4gb-jp441.zip](https://drive.google.com/file/d/1MAX1ibJvcLulKQeMtxbjMhsrOevBfUJd/view)|
> 2. 如果開機時進入的是 command line 模式, 可以參考以下指令, 進入 GUI 模式 https://imadelhanafi.com/posts/jetson_nano_setup/
因為, 待會兒的 examples 程式之一 teleoperation 需要用到遊戲手把 🎮 控制器, 我在 Mac 上操作 notebook 時有問題, 只有在 Jetbot 上直接執行時才 okay.
```
# disable GUI on boot
# After applying this command, the next time you reboot it will be on terminal mode
$ sudo systemctl set-default multi-user.target
# To enable GUI again
$ sudo systemctl set-default graphical.target
```
> 3. login 的 id 跟 password 都是 jetbot
> 4. 設定 wifi 的 command line 指令, 要記得 reboot 才能生效
```
$ sudo nmcli device wifi connect <SSID> password <PASSWORD>
$
```
> 5. 重新開機後, 先到 Jetbot 的 LED 上查看 wlan 的 IP 位址, 我查到的是 192.168.1.16
> 6. 到 PC 或 Mac 的 browers, 打開 http://<jetbot_ip_address>:8888 (我的例子就是 http://192.169.1.16:8888). 或者是直接在 Jetbot 上執行, 需要進入 jetbot 的 GUI 模式, 打開 browser, 輸入 http://localhost:8888

