from flet import *
from datetime import datetime
import time

import constants
from calcTimeDifference import calculate_time_difference

user_set_alarms = []


def main(page: Page) -> None:
    # PAGE SETUP
    page.title = 'Alarm Clock'
    page.theme_mode = 'light'
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.window_height = constants.MOBILE_HEIGHT
    page.window_width = constants.MOBILE_WIDTH
    page.scroll = ScrollMode.AUTO
    page.padding = 0
    page.fonts = constants.APP_FONTS
    page.theme = Theme(font_family='QS Regular')

    # To get all the values in the Text Fields
    def get_values(e):
        hour_value = page.views[1].controls[0].content.controls[1].content.controls[0].value
        minutes_value = page.views[1].controls[0].content.controls[1].content.controls[1].value
        am_pm_value = page.views[1].controls[0].content.controls[1].content.controls[2].value
        alarm_label = page.views[1].controls[0].content.controls[2].content.controls[0].value

        # Input fields validation
        # Checks if the values in TextField not empty
        if hour_value and minutes_value and am_pm_value and alarm_label:
            hours = int(hour_value)
            minutes = int(minutes_value)

            # Checks if the values in TextField is valid Time
            if hours > 12 or hours < 1 or minutes > 59 or minutes < 0:
                # If it's invalid, clear input field
                page.views[1].controls[0].content.controls[1].content.controls[0].value = ''
                page.views[1].controls[0].content.controls[1].content.controls[1].value = ''
                page.views[1].controls[0].content.controls[1].content.controls[2].value = ''
                page.views[1].controls[0].content.controls[2].content.controls[0].value = ''
                return

            # Creating the alarm UI
            alarm_str = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)} {am_pm_value}"
            alarm_label = alarm_label.capitalize()
            time_difference = calculate_time_difference(alarm_str)

            # Creating new alarm
            new_alarm = Container(
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            controls=[
                                Text(f'{alarm_label}', size=16, font_family='QS Light'),
                                Text(f'{alarm_str}', size=21, font_family='QS Medium'),
                                Text(f'{time_difference}', size=12)
                            ]
                        ),
                        Switch(value=False, active_track_color=constants.ACT, inactive_track_color=colors.WHITE)
                    ]
                ),
                padding=padding.all(16),
                bgcolor=constants.PRIM,
                border_radius=8
            )

            # Get the initial value of switch value of the newly created alarm
            switch_value = new_alarm.content.controls[1]
            # Get the current number of alarms in the alarms container
            current_number_of_alarms = len(main_content.controls[2].content.controls)

            # Record a new alarm with the following properties
            # This is used to track the alarm in the realtime update
            new_set_alarm = {
                'alarm': alarm_str,
                'label': alarm_label,
                'switch': switch_value,
                'time_difference': time_difference,
                'alarm_position': current_number_of_alarms + 1
            }
            # Add the new alarm tracker
            user_set_alarms.append(new_set_alarm)

            # Add the alarm widget in the container
            main_content.controls[2].content.controls.append(new_alarm)
            # Go back to previous page
            page.go('/')

        # Update the page
        page.update()

    # This functions runs infinitely to get the realtime update of the time and data
    def update_time_date():
        # Get the updated current time and date
        updated_current_time = datetime.now(constants.ph_time_zone).strftime('%I:%M %p')
        updated_current_date = datetime.now(constants.ph_time_zone).strftime('%B %d, %Y')

        # Loop through the alarms of a user
        for alarm in user_set_alarms:
            # Update the time difference of user alarm base on the alarm position
            alarm['time_difference'] = calculate_time_difference(alarm['alarm'], updated_current_time)
            current_alarm = alarm['alarm_position']
            main_content.controls[2].content.controls[current_alarm - 1].content.controls[0].controls[2].value = (
                alarm)['time_difference']

            # Checks if the specific alarm if turned on
            if alarm['switch'].value is True:
                set_alarmed = alarm['alarm']

                # Check if the turned on alarm is equal to current time
                if updated_current_time == set_alarmed:

                    dlg = AlertDialog(
                        title=Text("Alarm Notification 🔔"),
                        content=Text(f"{alarm['alarm']} - {alarm['label']}"),
                        actions_alignment=MainAxisAlignment.CENTER)
                    page.dialog = dlg
                    dlg.open = True
                    alarm['switch'].value = False

        # Update the current date and time to the UI
        main_content.controls[0].controls[1].value = f"{updated_current_date} {updated_current_time}"

        # Update the page
        page.update()

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()
        page.views.append(
            # If the route is "/" displays the UI of the current route
            View(
                '/',
                controls=[
                   main_container
                ]
            )
        )

        # If the user wants to create alarm, this will be displayed
        if page.route == '/create_alarm':
            page.views.append(
                View(
                    '/create_alarm',
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    # UI for back button in routes
                                    Column(
                                        controls=[
                                            IconButton(
                                                icon=icons.ARROW_BACK_IOS,
                                                on_click=lambda _: page.go('/')),
                                        ]
                                    ),
                                    # The TextFields for creating an Alarm Clock
                                    Container(
                                        content=Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                TextField(label='Hour', width=100),
                                                TextField(label='Minutes', width=100),
                                                Dropdown(
                                                    width=80,
                                                    options=[
                                                        dropdown.Option("AM"),
                                                        dropdown.Option("PM"),
                                                    ],
                                                )
                                            ]
                                        ),
                                        margin=margin.only(top=64)
                                    ),
                                    # UI for label of the alarm
                                    Container(
                                        content=Column(
                                            controls=[
                                                TextField(
                                                    label='Label',
                                                    border=InputBorder.UNDERLINE,
                                                    width=200,
                                                    dense=True)
                                            ]
                                        ),
                                        alignment=alignment.center
                                    ),
                                    # UI of cancel and save button
                                    Container(
                                        content=Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton('Cancel', on_click=lambda _: page.go('/')),
                                                ElevatedButton('Save', on_click=get_values),
                                            ]
                                        ),
                                        margin=margin.only(top=20)
                                    )
                                ]
                            ),
                            bgcolor=constants.BG,
                            height=constants.MOBILE_HEIGHT,
                            width=constants.MOBILE_WIDTH
                        ),
                    ]
                )
            )

        page.update()

    main_content = Column(
        controls=[
            Column(
                controls=[
                    Text('Today', size=40, font_family='QS Bold'),
                    Text(
                        f'{constants.current_date}  {constants.current_time}',
                        size=16,
                        font_family='QS Regular',
                        color=constants.SCD),
                ]
            ),
            Container(
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text('Alarms', size=21, font_family='QS SemiBold'),
                        IconButton(icon=icons.ADD, on_click=lambda _: page.go('/create_alarm'))
                    ],
                ),
                margin=margin.only(top=16),
            ),
            Container(
                content=Column(
                    spacing=8,
                    scroll=ScrollMode.AUTO,
                    controls=[
                        # All new Alarms goes here
                    ]
                ),
                height=470
            ),
        ]
    )

    main_container = Container(
        bgcolor=constants.BG,
        content=Stack(
            controls=[
                # Inject main content
                main_content
            ]
        ),
        padding=padding.symmetric(vertical=16, horizontal=24),
        height=constants.MOBILE_HEIGHT,
        width=constants.MOBILE_WIDTH
    )

    page.on_route_change = route_change
    page.go(page.route)

    while True:
        update_time_date()
        time.sleep(1)


app(target=main, view=FLET_APP)
