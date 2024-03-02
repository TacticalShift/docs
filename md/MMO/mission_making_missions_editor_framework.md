@Meta(Position=2 ) NORENDER
@Keywords(mmo) NORENDER

# Tactical Shift Framework

## Обзор и знакомство Tactical Shift Mission Framework

Миссии на Tactical Shift создаются с использованием 4х скриптовых компонент:

- ^dzn_dynai^
Скрипт генерации и поведения AI (патрули, подкрепления).
- ^dzn_gear^
Скрипт для выдачи преднастроенного снаряжения AI юнитам, игрокам и технике. Интегрирован в dzn_dynai.
- ^tSFramework^
Набор sqf-скриптов для поддержки базовой логики миссии, а также утилиты для создания брифингов, эндингов и проч.
- ^dzn_brv^
Скрипт для логирования игровой сессии (см. [tS AARs](https://tacticalshift.ru/aar/))

Этих компонентов достаточно для создания большинства миссий в короткий срок. Тем не менее вы можете использовать любые иные скриптовые решения (впрочем, желательно интегрироваться с ^dzn_brv^, для создания AAR по вашей миссии).

## Порядок установки tSFramework

Инсталлятор:

1. Скачать и установить последнюю версию [Java](https://www.java.com/ru/download/help/windows_manual_download.xml)
2. Скачать и распаковать [tSF_Installer](https://github.com/10Dozen/tSF_Installer/archive/master.zip)
3. Запустить tSF_Installer_(version).jar
4. Выбрать путь до папки вашей миссии, выбрать нужные компоненты (при необходимости указав бранч), выбрать нужные киты из [коллекции](https://github.com/rempopo/Gear_Kits_Collection) (скопировать ссылку KitLink нужного набора)

Руками:

1. Скачать:
    - [dzn_dynai](https://github.com/10Dozen/dzn_dynai)
    - [dzn_gear](https://github.com/10Dozen/dzn_gear)
    - [tS Framework (включает dzn_brv)](https://github.com/10Dozen/dzn_tSFramework)
2. Распакуйте архивы в отдельные папки, а затем скопируйте содержимое каждого архива в папку с вашей миссии (в порядке скачивания). Подтвердите замену всех файлов.

## Из чего состоит tSFramework

Ссылка: [GitHub](https://github.com/10Dozen/dzn_tSFramework)
tSFramework это набор sqf-скриптов и html-утилит для создания миссий в Arma 3.
HTML - утилиты также доступны [в интернетах](https://10dozen.github.io/A3WebHelpers/)
*[HTML]: Hyper Text Markup Language

Рассмотрим этот фреймворк:

- ^MIG^
Рандомизатор заданий. Если нет идей о чем делать миссию, покрути рулетку.
- ^3DEN Tool^
См. [Обзор tSF 3DEN Tool](https://docs.google.com/presentation/d/1-hwUq2sYlP9BzIy4GzOBALAaTHpBOzPOXhZyXPhatXQ/edit?usp=sharing)
Скрипт расширяющий функциональность 3DEN (3д редактор Армы 3). С помощью этого скрипта вы сможете быстро расставить преднастроенных игровых юнитов (согласно выбранной доктрине), разместить зоны dzn_dynai, добавить настроенный модуль Zeus, преднастроить миссию для JIP-совместимости, добавить к юнитам созданным в редакторе специфичные настройки dzn_gear/dzn_dynai
- ^Airborne Support^
Модуль воздушного транспорта (AI)
- ^Briefing^
Утилита для создания брифинга в стандартном формате, а также скрипт для отображения брифинга.
- ^CCP^
Скрипт позволяющий в течении игрового брифинга установить точку сбора раненых, где раненные могут быть излечены.
- ^Editor Radio Settings^
Модуль для установки определенного TFAR радио на технику (например, для добавления раций BLUFOR на машины другой фракции)
- ^Editor Unit Behavior^
Модуль для добавления юниту возможности сдаваться (для сценарных персонажей)
- ^Editor Vehicle Crew^
Модуль для создания экипажа технике установленной в редакторе (например, экипаж из одного стрелка), с возможность назначения dzn_gear кита и dzn_dynai поведения типа vehicle hold
- ^Interactives^
Скрипт исполняющий ваш код на выбранных объектах или объектах указанных классов. Например, если вы хотите добавить ко всем ящикам в миссии определенное действие.
- ^Interactives ACE^
Скрипт добавляющий кастомизированные ACE Interaction и ACE Self-Interaction действия на объекты или классы.
- ^Intro Text^
Скрипт для отображения интро-текста в начале миссии.
- ^JIP Teleport^
Добавляет возможность JIP игрокам самостоятельно телепортироваться к своему лидеру отряда.
- ^Mission Conditions^
Скрипт следящий за исполнением условий завершения миссии и завершающий миссиию согласно указанным концовкам. Также утилита для генерации классов концовок.
- ^Mission Defaults^
Кое-какие обязательные скрипты, а также временное отключение управления игрой на старте миссии (чтобы облегчить серверу старт миссии).
- ^Platoon Operationl Markers^
Добалвяет возможность лидеру взвода добавлять, перемещать и удалять маркеры видимые только для него.
- ^tSAdminTools^
Набор инструментов для залогиненного админа - выдача снаряжения, принудительное завершение миссии.
- ^tSNotes^
Скрипт добавляющий топик с дополнительными инструкциями (формат радиоотчетов, формат запроса CAS, артиллерийского удара и т.п.)
- ^tSNotesSettings^
Скрипт добавляющий топик с настройами дальности видимости

## Работа с tSFramework

### 3DEN Tool

См. [Обзор tSF 3DEN Tool](https://docs.google.com/presentation/d/1-hwUq2sYlP9BzIy4GzOBALAaTHpBOzPOXhZyXPhatXQ/edit?usp=sharing)

### Briefing

Расположение модуля: ^dzn_tSFramework/Modules/Briefing/^
При помощи BriefingHelper создайте файл брифинга и замените им файл ^tSF_briefing.sqf^. О требованиях к брифингу читайте [тут](https://tacticalshift.ru/docs/MMO/mission_making_missions_editor_requirements.html).

### CCP

Расположение модуля: ^dzn_tSFramework/Modules/CCP/^
Разместите все необходимые триггеры и свяжите их (синхронизация) с объектом tsf_CCP.
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_CCP_TimeToHeal^ – время в секундах для полного излечения игрока на CCP
- ^tSF_CCP_TimeToHold^ – время в секундах, которое игрок вынужден провести на CCP после излечения
- ^dzn_tsf_CCP_DefaultComposition^ – название композиции (набора объектов), которая будет размещена в зоне CCP (список названий можно посмотреть в файле DefaultCompositions.sqf)

### EditorVehicleCrew

Расположение модуля: ^dzn_tSFramework/Modules/EditorVehicleCrew/^
Используйте 3DEN Tool для создания связки с юнитами.
Произведите настройку модуля в файле ^Settings.sqf^ - таблица в формате: [ @Название, [@Роли ('driver','gunner','commander'), @Сторона, @Навык (0…1), @Набор dzn_gear ]]

### Interactives

Расположение модуля: ^dzn_tSFramework/Modules/Interactives/^
В файле Settings.sqf есть только массив в котором можно указать объекты и код, который нужно на них выполнить. Рассмотрим по-ближе как выглядит элемент данного массива:
^`[ [″Land_ToiletBox_F″], { _this addAction [″Check″, {hint ″This is the toilet box″;}] }, ″client″, true ]`^
, где:

- ^[″Land_ToiletBox_F″]^ – список классов или имен объектов, для которых будет выполнен кол;
- ^{ _this addAction [″Check″, {hint ″This is the toilet box″;}] }^ – sqf-код, который будет выполнен. ^_this^ в коде будет ссылкой на сам объект.
- ^″client″^ – где будет выполнен код - только на клиентах-игроках ^(client)^, только на сервере ^(server)^ или везде ^(global)^
- ^true^ – если ^true^, то код будет выполняться также для всех объектов указанных классов, которые будут созданы в течении игры (например, зевсом или объекты которые игроки выкинули из своего инвентаря).

### Interactives ACE

Расположение модуля: ^dzn_tSFramework/Modules/InteractivesACE/^
В файле ^Settings.sqf^ есть только массив в котором можно указать описать добавляемый действия. Действия бывают 2 типов - для self-interaction меню и для interaction (т.е. на других объектах) - и 2 уровней вложенности (в первичном меню по кнопке WIN / CTRL+WIN или в подменю).
Рассмотрим по-ближе как выглядят элементы данного массива:
^[ ″SELF″, ″Check my ass″, ″ass_action_core″, ″″, { hint ″Your ass is OK″ }, { true }]^
^[ ″SELF″, ″Check my ass more closely″, ″ass_action_extra″, ″ass_action_core″, { hint ″Your ass is OK″ }, { true }]^
, где:

- ^[″SELF″]^ – тип действия: SELF - для self-interaction menu; [@Classnames] - список классов для interaction menu;
- ^″Check my ass″^ – отображаемое название;
- ^″ass_action_core″ / ″ass_action_extra″^ – идентификатор действия;
- ^″″ / ″ass_action_core″^ – идентификатор родительского действия (если ″″ – действие добавится в корневое меню);
- ^{ hint ″Your ass is OK″ }^ – код выполняемый при вызове действия (_target – ссылка на объект к которому привязано действие);
- ^{ true }^ – условие отображения действия.

### Intro Text

Расположение модуля: ^dzn_tSFramework/Modules/CCP/^
Разместите все необходимые триггеры и свяжите их (синхронизация) с объектом tsf_CCP.
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_Intro_ShowCurrentTime^ – если true, то в первой линии будет отображаться текущее время в формате h:mm (8:00, 23:00)
- ^tSF_Intro_LineText1^ – текст первой линии, Дата вида 31/12/2016 (или %1/%2/%3 если вы хотите использовать дату заданную в настройках миссии)
- ^tSF_Intro_LineText2^ – текст второй линии, Место вида Шукуркалай, Центральный Такистан
- ^tSF_Intro_LineText3^ – текст третьей линии, Название вида Операция 'Восход'

### JIP Teleport

Расположение модуля: ^dzn_tSFramework/Modules/JIPTeleport/^
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_JIPTeleport_MaxTime^ – время в течение которого для JIP игрока будет доступен телепорт к лидеру своего отряда;
- ^tSF_JIPTeleport_MaxDistance^ – радиус покинув который игрок потеряет возможность телепортироваться к лидеру своего отряда;
- ^tSF_JIPTeleport_RelativePos^ – относительная позиция (от лидера отряда) куда будет перемещен игрок;

### Mission Conditions

Расположение модуля: ^dzn_tSFramework/Modules/MissionConditions/^
При помощи EndingsHelper создайте файл концовок (дебрифингов) и замените им файл ^Endings.hpp^.
Произведите настройку модуля в файле ^Settings.sqf^:

- ^PlayersBaseTrigger^ – укажите имя триггера, который будет обозначать зону возврата для игроков (для проверки того, что игроки вернулись в заданную зону - используйте функцию ^call fnc_CheckPlayersReturned^ или проверяйте локацию ^BaseLoc^). Если вам не нужна такая проверка, то укажите пустую строку.
- ^tSF_MissionCondition_DefaultCheckTimer^ – интервал по-умолчанию для проверки условий завершения миссии
- ^MissionCondition1^ – массив условия миссии в виде ^[ ″WIN″, ″MVP inArea BaseLoc && alive MVP″, ″All objectives done″, 15 ]^. Вы можете добавить до 20 условий, указав дополнительные переменные с именем MissionCondition1 … MissionCondition20.
Рассмотрим из чего состоит массив условия:
^[ ″WIN″, ″MVP inArea BaseLoc && alive MVP″, ″All objectives done″, 15 ]^
, где:

1. ^″WIN″^ – название класса концовки (содержащейся в Endings.hpp);
2. ^″MVP inArea BaseLoc && alive MVP″^ – sqf-код условия, который после выполнения должен возвращать ^true^ или ^false^. Подробнее об условиях можно прочитать в примерах Mission Conditions;
3. ^″All objectives done″^ – короткое текстовое описание концовки для отображения в tSAdminTools;
4. ^15^ – опциональный параметр, интервал для проверки условий завершения мисии. Если не указан, то используется значение ^tSF_MissionCondition_DefaultCheckTimer^.

### Mission Defaults

Расположение модуля: ^dzn_tSFramework/Modules/MissionDefaults/^
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_MissionDefaults_DisableInputOnStart^ – если ^true^, то отключает управление на старте миссии (облегачает запуск миссии на сервере).
- ^tSF_MissionDefaults_DisableInputTimer^ – время на которое будет отключено управление.
- ^tSF_MissionDefaults_SubtitleText^ – текст, отображающийся на время отключения управления.
- ^tSF_MissionDefaults_PutEarplugsOn^ – принудительно добавляет и вставляет беруши (ACE).
- ^tSF_MissionDefaults_PutWeaponSafe^ – принудительно ставит оружие игрока на предохранитель (ACE).

### Platoon Operational Markers (POM)

Расположение модуля: ^dzn_tSFramework/Modules/POM/^
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_POM_AuthorizedUsers^ – список ролей (названий слотов) для которых будет доступен интерфейс POM;
- ^tSF_POM_GenerateMarkersFromGroups^ – нужно ли создавать маркеры для отрядов игроков;
- ^tSF_POM_OperationalMarkers^ – предварительно заданные маркеры (в формате [ @Тип (“Intantry”/“Vehicle”), @Название, @Сторона (west,east…), @Защита от редактирования (true/false)]);
- ^tSF_POM_TopicName^ – название топика на экране карты;
- ^tSF_POM_InfantryMarker^ и tSF_POM_VehicleMarker – класс маркера для типа Infantry и Vehicle, соответственно;
- ^tSF_POM_InfantryLabels^ и tSF_POM_VehicleLabels – доступные названия маркеров для типа Infantry и Vehicle, соответственно.

### tSAdminTools

Расположение модуля: ^dzn_tSFramework/Modules/tSAdminTools/^
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_AdminTools_TopicName^ – отображаемое название темы на экране карты\брифинга.
- ^tSF_AdminTool_EnableMissionEndings^ – если true, то позволяет администратору принудительно завершать миссию одной из общих концовок, либо концовкой настроенной в модуле Mission Conditions.
- ^tSF_AdminTool_EnableGATTool^ – если true, то позволяет администратору выдавать преднастроенные в dzn_gear наборы снаряжения игрокам (только те из них, которые были использованы в Gear Assignment Table)

### tSNotes

Расположение модуля: ^dzn_tSFramework/Modules/tSNotes/^
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_note_displayName^ – отображаемое название темы на экране карты\брифинга.
- ^tSF_note_enableAdvancedMedicine^ – если ^true^, то добавляет краткую инструкцию о работе ACE Advanced Medicine.
- ^tSF_note_enableReports^ – если ^true^, то добавляет заметку о форматах радиоотчетов.
- ^tSF_note_enableNineliner^ – если ^true^, то добавляет заметку о формате 9-liner (вызов CAS).
- ^tSF_note_enableArtilleryControl^ – если ^true^, то добавляет заметку о запросе артиллерийского огня.
- ^tSF_note_enableMEDEVAC^ – если ^true^, то добавляет заметку о формате вызова медицинской эвакуации.

### tSNotesSettings
Расположение модуля: ^dzn_tSFramework/Modules/tSNotesSettings/^
Произведите настройку модуля в файле ^Settings.sqf^:

- ^tSF_noteSettings_displayName^ – отображаемое название темы на экране карты\брифинга
- ^tSF_noteSettings_enableViewDistance^ – если ^true^, то добавляет возможность изменять дальность прорисовки
