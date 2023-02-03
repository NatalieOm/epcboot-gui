# EPCboot GUI

Описание не русском языке можно найти ниже.



## **Brief description**

EPCboot GUI is a cross–platform software with a graphical interface for updating the firmware of devices manufactured by EPS MSU. 

EPCboot GUI is distributed both as Python source codes and as binary releases. Supports Windows and Linux operating systems.



## **User Manual** 

1. Go to the program directory.

2. Run the EPCboot GUI program: click on the executable file, or run the command from the command line (`epcboot_gui.exe ` on windows, `./epcboot_gui` on Linux).

3. Select the COM port from the drop-down list. The COM port number can be viewed in the device manager on Windows or in the /dev directory on Linux (the device will most likely have a name in the ttyACMx format, where x is the device number).

4. Click "Browse" and specify the path to the firmware file. The firmware file has the .cod extension, is included in the software package supplied with the device, can also be downloaded from the official website physlab.ru .

5. Start the update with the "Update firmware" button and wait for it to finish. In the Log block, the inscription "INFO - Ok" will appear when the update is successful.

The functions from the Developer block are used in the production of equipment. If you are not engaged in the manufacture or repair of equipment, please do not use them. The functions contained in this block can lead to the loss of the firmware without the possibility of reinstalling it.

If you are a device developer, a guide to using the features of the Developer block is located below.

#### **Possible errors and warnings**

To track the progress of the EPCboot GUI program, please use the program Log block.

Possible causes of error messages and warnings (starting with the words ERROR or WARNING):

1. The COM port is busy. 

​	The COM port selected in the EPCboot GUI program can already be used in another application. Please 	release the port and try the update again.

2. The COM port occupied by another device is selected.

​	Follow step 3 of the "User Manual" section.

3. The device is not connected.

​	Please make sure that the device is turned on and properly connected to the computer.

4. The device driver is not installed.

​	Install the appropriate driver. The driver is included in the software package supplied with the device,            and can also be downloaded from the official website [physlab.ru]().

#### **Note for Linux users**

• If an error occurs with access permission, allow execution by running the command in the terminal: 

 ```bash
 chmod ugo+x epcboot_gui
 ```

• To work correctly with COM ports, a user (with the name `username`) must be added to the "dialout" group. To add a user, run the command:

 ```bash
 sudo adduser username dialout
 ```

• On Linux machine we recommend to stop (or remove) the ModemManager. The ModemManager interferes with our bootloader.

```bash
sudo systemctl stop ModemManager.service
```



##  **Device Developer’s Manual**

The initial installation of the firmware and its update is performed in accordance with the steps described in the "User Manual" section.

Important! Installing an incorrect key may prevent the firmware from being updated. In addition, using the functions of this unit will void the warranty of the device. If you are not sure of of what to do, contact the device manufacturer.

#### **Uploading the encryption key file to the controller**

In the EPCboot GUI program, follow the steps:

1. Connect the device to the program as described above in the "User Manual" section.

2. Check the checkbox "Developer mode".

3. In the "Key" block, click the "Browse" button and specify the path to the .txt key file.

4. Press the "Set key" button to load it into the controller.

#### **Serial number and version update**

Setting the serial number and version of the device without specifying the encryption key does not work. Make sure that the steps described in the previous section are completed.

Follow the steps:

1. Enter the serial number in the appropriate field.

2. Check the "Auto increment" checkbox if you want to download the firmware to multiple devices. This will automatically increase the serial number by one and simplify the work.

3. Enter the firmware version in the "HW Version" field and click "Install serial number and hardware version".



## **Software Developer's Manual**

The steps for building a binary release on Windows and Linux are described below. This section is intended for software developers.

#### **Building a Windows binary release**

In the epcboot-gui directory in command prompt/powershell build:

- with console for debugging

```
.\release_win64.bat --console
```

- without console

```bash
.\release_win64.bat --noconsole
```

#### **Building a Linux binary release**

In the epcboot-gui directory in terminal build:

```bash
source release.sh
```

#### **Run (python)**

In the epcboot-gui directory in cmd/powershell for Windows or terminal for Linux:

 ```bash
 python -m pip install -r requirements.txt
 cd epcboot_gui
 python epcboot_gui.py
 ```

NOTE

- tkinter and python3-venv on linux should be installed. If not, do so:

 ```bash
 sudo apt install python3-tk python3-venv
 ```

- On Linux machine we recommend to stop (or remove) the modemmanager. The modemmanager interferes with our bootloader.

```bash
sudo systemctl stop ModemManager.service
```

This repository is configured to build automatically. Find build artifacts here https://github.com/EPC-MSU/epcboot-gui/actions?query=workflow%3ABuild. Use them when creating a release.

------



## **Краткое** **описание**

EPCboot GUI – кроссплатформенное программное обеспечение с графическим интерфейсом для обновления прошивок устройств, выпускаемых ЦИФ МГУ. 

EPCboot GUI распространяется как в виде исходных кодов на языке Python, так и в виде бинарных релизов. Поддерживает операционные системы Windows и Linux.



## **Руководство пользователя**

#### **Обновление прошивки**

1. Перейдите в директорию программы.

2. Запустите программу epcboot_gui, кликнув по исполняемому файлу, либо выполнив команду через командную строку (`epcboot_gui.exe` на windows, `./epcboot_gui` на Linux).

3. Выберите из выпадающего списка COM-порт. Номер COM-порта можно посмотреть в диспетчере устройств ОС Windows или в директории /dev в ОС Linux (устройство, скорее всего, будет иметь имя в формате ttyACMx, где x – номер устройства).

4. Нажмите «Browse» и укажите путь к файлу прошивки. Файл прошивки имеет расширение .cod, входит в комплект ПО, поставляемый вместе с устройством, также может быть загружен с официального сайта [physlab.ru]().

5. Запустите обновление кнопкой «Update firmware» и дождитесь его окончания. При успешном обновлении в блоке Log появится надпись "INFO - Ok". 

Функции из блока Developer используются на производстве оборудования. Если вы не занимаетесь производством или ремонтом оборудования, пожалуйста, не используйте их. Функции, находящиеся в данном блоке, могут привести к потере прошивки без возможности её повторной установки. 

Если вы разработчик устройств, руководство по использованию возможностей блока Developer расположено ниже.

#### **Возможные ошибки и предупреждения**

Для отслеживания хода работы программы EPCboot GUI воспользуйтесь блоком Log программы. 

Возможные причины появления сообщений об ошибках и предупреждений (начинающихся со слов ERROR или WARNING): 

1. COM-порт занят. 

   Выбранный в программе EPCboot GUI COM-порт может быть уже использован в другом приложении. Освободите порт и повторите попытку обновления.

2. Выбран занятый другим устройством COM-порт.

   Выполните шаг 3 раздела «Руководство пользователя».

3. Устройство не подключено.

   Убедитесь, что устройство включено и правильно соединено с компьютером. 

4. Не установлен драйвер устройства.

   Установите подходящий драйвер. Драйвер входит в комплект ПО, поставляемый вместе с устройством, а также может быть загружен с официального сайта physlab.ru.

#### **Примечание для пользователей** **Linux**

- Если возникает ошибка с разрешением доступа, разрешите выполнение, запустив команду в терминале:

```bash
chmod ugo+x epcboot_gui
```

- Пользователь должен быть добавлен в группу "dialout", чтобы приложение корректно работало с COM-портами. Чтобы добавить пользователя (с именем `username`) в эту группу, выполните команду:

```bash
sudo adduser username dialout
```

- Кроме того, мы рекомендуем остановить (или удалить) приложение ModemManager, так как оно вмешивается в работу нашего загрузчика.

```bash
sudo systemctl stop ModemManager.service
```



## **Руководство для разработчиков устройств**

Первичная установка прошивки и её обновление производится в соответствии с шагами, описанными в разделе «Руководство пользователя». 

**Важно!** Установка неправильного ключа может привести к невозможности обновления прошивки. Кроме того, при использовании функций из данного блока устройство снимается с гарантии. Если вы не уверенны в своих действиях, обратитесь к производителям устройства.

#### **Загрузка файла ключа шифрования в контроллер**

В программе EPCboot GUI выполните шаги:

1. Подключите устройство в программу, как было описано выше в разделе «Руководство пользователя». 

2. Отметьте флажком чекбокс «Developer mode». 

3. В блоке «Key» нажмите кнопку «Browse» и укажите путь к .txt файлу ключа.

4. Нажмите кнопку «Set key» для его загрузки в контроллер.

#### **Обновление серийного номера и версии**

Если путь до файла с ключом шифрования не указан, укажите его (см. предыдущий раздел). Установка серийного номера и версии устройства без указания ключа не работает.

Выполните шаги:

1. Введите серийный номер в соответствующее поле. 

2. Для упрощения работы при массовой прошивке устройств для автоматического увеличения серийного номера на единицу, отметьте флажком чекбокс «Auto increment». 

3. Введите версию прошивки в поле «HW version» и нажмите кнопку «Set serial number and hardware version».



## **Руководство для разработчиков программного обеспечения**

Ниже описаны шаги для сборки бинарного релиза в Windows и Linux. Данный раздел предназначен для разработчиков программного обеспечения.

#### **Сборка бинарного релиза Windows**

В папке epcboot-gui в командной строке 

Сборка с консольным выводом для отладки:

```bash
.\release_win64.bat --console
```

Сборка графического приложения без отладочной консоли:

```bash
.\release_win64.bat --noconsole
```

#### **Сборка бинарного релиза Linux**

В каталоге epcboot-gui при сборке в терминале выполнить команду:

```bash
source release.sh
```

#### **Запуск (python)**

В папке epcboot-gui в cmd/powershell для Windows или в терминале для Linux:

```bash
python -m pip install -r requirements.txt
cd epcboot_gui
python epcboot_gui.py
```

#### **Примечание**

- Должны быть установлены библиотеки tkinter и python3-venv в ОС Linux. Если их нет, выполните команду:

```bash
sudo apt install python3-tk python3-venv
```

- Мы рекомендуем остановить (или удалить) приложение ModemManager, так как оно вмешивается в работу нашего загрузчика.

```bash
sudo systemctl stop ModemManager.service
```

Этот репозиторий настроен на автоматическую сборку. При создании релиза используйте артефакты сборки, которые можно найти здесь https://github.com/EPC-MSU/epcboot-gui/actions?query=workflow%3ABuild.
