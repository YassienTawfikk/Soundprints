import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets

# ------------------------------------------------------------------------
#                           Global Constants
# ------------------------------------------------------------------------
MAIN_COLOR = "#455054"
SECONDARY_COLOR = "#FFF"

WINDOW_STYLE = f"background-color:{MAIN_COLOR}"
BUTTON_STYLE = """
    QPushButton {
        color: #fff;
        background-color: rgba(255, 255, 255, 0);
        border: 3px solid #fff;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 10);
    }
"""
LABEL_WHITE_TEXT = f"color:{SECONDARY_COLOR}"
GROUPBOX_WHITE_TEXT = f"color:{SECONDARY_COLOR}"

TITLE_FONT = QtGui.QFont("Didot", 30)
SIDEBAR_TITLE_FONT = QtGui.QFont("Didot", 25)
SECTION_FONT = QtGui.QFont("Didot", 18)
ITEM_NAME_FONT = QtGui.QFont("Didot", 14)


class Ui_MainWindow(object):
    """
    This class sets up the main window UI components with reusable helpers.
    All QGroupBox, QPushButton, and QLabel objects are stored as self.<variable_name>
    so you can access them in other files or code sections.
    """

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(WINDOW_STYLE)
        MainWindow.setWindowTitle("MainWindow")  # Set title directly

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ------------------ Title Bar ------------------ #
        self.setup_title_bar()

        # ------------------ Side Bar ------------------- #
        self.setup_side_bar()

        # ------------------ Recognized Song Data ------- #
        self.setup_recognized_song_data()

        # ------------------ Recognize Song Bar --------- #
        self.setup_recognize_song_bar()

        # ------------------ Spectrogram Group Box ------ #
        self.setup_spectrogram_group()

        # ------------------ Quit Button ---------------- #
        self.setup_quit_button()

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ------------------------------------------------------------------------
    #                           UTILITY METHODS
    # ------------------------------------------------------------------------
    def create_label(self, parent, text="", geometry=None, max_size=None, font=None, style_sheet="", alignment=None):
        """
        Utility to create a QLabel, assign it as self.<var_name>,
        and set the text/styles directly.
        """
        label = QtWidgets.QLabel(parent)
        label.setText(text)

        if geometry is not None:
            label.setGeometry(geometry)
        if max_size is not None:
            label.setMaximumSize(max_size)
        if font is not None:
            label.setFont(font)
        if style_sheet:
            label.setStyleSheet(style_sheet)
        if alignment is not None:
            label.setAlignment(alignment)

        return label

    def create_button(self, parent, text="", geometry=None, max_size=None, font=None, style_sheet="", cursor=None):
        """
        Utility to create a QPushButton, assign it as self.<var_name>,
        and set the text/styles directly.
        """
        button = QtWidgets.QPushButton(parent)
        button.setText(text)

        if geometry is not None:
            button.setGeometry(geometry)
        if max_size is not None:
            button.setMaximumSize(max_size)
        if font is not None:
            button.setFont(font)
        if style_sheet:
            button.setStyleSheet(style_sheet)
        if cursor is not None:
            button.setCursor(cursor)

        return button

    def create_graph(self, group_box):
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground(f'{MAIN_COLOR}')

        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(plot_widget)
        group_box.setLayout(graph_layout)

        # Configure plot item within the widget
        plot_item = plot_widget.getPlotItem()
        plot_item.hideButtons()
        # plot_item.getViewBox().setMouseEnabled(x=False, y=False)
        plot_item.getAxis('left').setLabel('Frequency (Hz)')
        plot_item.getAxis('bottom').setLabel('Time (s)')

        return plot_widget

    # ------------------------------------------------------------------------
    #                           UI SETUP HELPERS
    # ------------------------------------------------------------------------
    def setup_title_bar(self):
        """
        Creates the top title bar with an icon and a label.
        """
        # Container
        self.layout_widget_title_bar = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget_title_bar.setGeometry(QtCore.QRect(280, 0, 271, 91))
        self.layout_widget_title_bar.setObjectName("layout_widget_title_bar")

        # Horizontal Layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layout_widget_title_bar)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Icon
        self.title_icon = QtWidgets.QLabel(self.layout_widget_title_bar)
        self.title_icon.setObjectName("title_icon")
        self.title_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.title_icon.setPixmap(QtGui.QPixmap("static/images/Fingerprint.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.title_icon)

        # Label
        self.title_label = self.create_label(
            parent=self.layout_widget_title_bar,
            text="Soundprints",
            max_size=QtCore.QSize(179, 38),
            font=TITLE_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.horizontalLayout.addWidget(self.title_label)

    def setup_side_bar(self):
        """
        Creates the left side bar with different sections (song, vocals, instruments),
        plus the Generate and Cancel buttons.
        """
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(10, 0, 261, 751))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")

        self.declare_song_side_bar = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.declare_song_side_bar.setContentsMargins(0, 0, 0, 0)
        self.declare_song_side_bar.setObjectName("declare_song_side_bar")

        # Sidebar Title
        self.sidebar_title = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Declare a Song",
            max_size=QtCore.QSize(240, 80),
            font=SIDEBAR_TITLE_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.declare_song_side_bar.addWidget(self.sidebar_title)

        # ========== Upload Complete Song ==========
        self.upload_songs_layout = QtWidgets.QVBoxLayout()
        self.upload_songs_layout.setObjectName("upload_songs_layout")

        self.upload_songs_label = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Enter Complete Song",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_songs_layout.addWidget(self.upload_songs_label)

        self.upload_song_button = self.create_button(
            parent=self.verticalLayoutWidget_8,
            text="Upload",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.upload_songs_layout.addWidget(self.upload_song_button)

        self.uploaded_song_name = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Wish You Were Here",
            max_size=QtCore.QSize(240, 17),
            font=ITEM_NAME_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_songs_layout.addWidget(self.uploaded_song_name)

        self.declare_song_side_bar.addLayout(self.upload_songs_layout)

        # ========== Upload Vocals ==========
        self.upload_vocals_layout = QtWidgets.QVBoxLayout()
        self.upload_vocals_layout.setObjectName("upload_vocals_layout")

        self.upload_vocals_label = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Enter Song Vocals",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_vocals_layout.addWidget(self.upload_vocals_label)

        self.upload_vocals_button = self.create_button(
            parent=self.verticalLayoutWidget_8,
            text="Upload",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.upload_vocals_layout.addWidget(self.upload_vocals_button)

        self.uploaded_vocals_name = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Wish You Were Here",
            max_size=QtCore.QSize(240, 15),
            font=ITEM_NAME_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_vocals_layout.addWidget(self.uploaded_vocals_name)

        self.declare_song_side_bar.addLayout(self.upload_vocals_layout)

        # ========== Upload Instruments ==========
        self.upload_instruments_layout = QtWidgets.QVBoxLayout()
        self.upload_instruments_layout.setObjectName("upload_instruments_layout")

        self.upload_instruments_label = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Enter Song Instruments",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_instruments_layout.addWidget(self.upload_instruments_label)

        self.upload_instruments_button = self.create_button(
            parent=self.verticalLayoutWidget_8,
            text="Upload",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.upload_instruments_layout.addWidget(self.upload_instruments_button)

        self.uploaded_instruments_name = self.create_label(
            parent=self.verticalLayoutWidget_8,
            text="Wish You Were Here",
            max_size=QtCore.QSize(240, 15),
            font=ITEM_NAME_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_instruments_layout.addWidget(self.uploaded_instruments_name)

        self.declare_song_side_bar.addLayout(self.upload_instruments_layout)

        # ========== Generate & Cancel ==========
        self.generate_cancel_layout = QtWidgets.QHBoxLayout()
        self.generate_cancel_layout.setObjectName("generate_cancel_layout")

        self.generate_sound_button = self.create_button(
            parent=self.verticalLayoutWidget_8,
            text="Generate",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.generate_cancel_layout.addWidget(self.generate_sound_button)

        self.cancel_button = self.create_button(
            parent=self.verticalLayoutWidget_8,
            text="Cancel",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.generate_cancel_layout.addWidget(self.cancel_button)

        self.declare_song_side_bar.addLayout(self.generate_cancel_layout)

    def setup_recognized_song_data(self):
        """
        Group box for showing recognized song data at the bottom.
        """
        self.recognized_song_data_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.recognized_song_data_groupBox.setGeometry(QtCore.QRect(480, 640, 520, 120))
        self.recognized_song_data_groupBox.setFont(QtGui.QFont("Didot"))
        self.recognized_song_data_groupBox.setStyleSheet(GROUPBOX_WHITE_TEXT)
        self.recognized_song_data_groupBox.setObjectName("recognized_song_data_groupBox")
        self.recognized_song_data_groupBox.setTitle("Song is Recognizing…")  # GroupBox title set directly

        # Title label inside groupbox
        self.upload_songs_label_4 = self.create_label(
            parent=self.recognized_song_data_groupBox,
            text="Wish You Were Here",
            geometry=QtCore.QRect(40, 30, 270, 70),
            max_size=QtCore.QSize(300, 80),
            font=SIDEBAR_TITLE_FONT,
            style_sheet=f"color:{SECONDARY_COLOR}; background-color:none;"
        )

        # Icon inside groupbox
        self.recognized_song_icon = QtWidgets.QLabel(self.recognized_song_data_groupBox)
        self.recognized_song_icon.setObjectName("recognized_song_icon")
        self.recognized_song_icon.setGeometry(QtCore.QRect(400, 30, 80, 79))
        self.recognized_song_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.recognized_song_icon.setStyleSheet("background-color:none")
        self.recognized_song_icon.setPixmap(QtGui.QPixmap("static/images/pinkfloyd.png"))
        self.recognized_song_icon.setScaledContents(True)
        self.recognized_song_icon.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)

    def setup_recognize_song_bar(self):
        """
        Creates the horizontal layout to let users choose an unknown song to recognize.
        """
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(630, 0, 451, 91))
        self.verticalLayoutWidget_9.setObjectName("recognized_song_layout")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.verticalLayoutWidget_9)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.recognize_song_label = self.create_label(
            parent=self.verticalLayoutWidget_9,
            text="Choose Unknown Song",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.horizontalLayout_2.addWidget(self.recognize_song_label)

        self.recognize_song_button = self.create_button(
            parent=self.verticalLayoutWidget_9,
            text="Upload Song",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.horizontalLayout_2.addWidget(self.recognize_song_button)

    def setup_spectrogram_group(self):
        """
        Group box for displaying the recognized song’s spectrogram.
        """
        self.recognized_song_spectrogram_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.recognized_song_spectrogram_groupBox.setGeometry(QtCore.QRect(280, 90, 981, 541))
        self.recognized_song_spectrogram_groupBox.setFont(QtGui.QFont("Didot"))
        self.recognized_song_spectrogram_groupBox.setStyleSheet(LABEL_WHITE_TEXT)
        self.recognized_song_spectrogram_groupBox.setObjectName("recognized_song_spectrogram_groupBox")
        self.recognized_song_spectrogram_groupBox.setTitle("Song Spectrogram")  # GroupBox title set directly

        self.plot_widget = self.create_graph(self.recognized_song_spectrogram_groupBox)

    def setup_quit_button(self):
        """
        Creates the quit button at the top-right corner of the window.
        """
        self.quit_app_button = self.create_button(
            parent=self.centralwidget,
            text="X",
            geometry=QtCore.QRect(1209, 20, 50, 50),
            max_size=QtCore.QSize(50, 50),
            style_sheet="""
                QPushButton { 
                    color: rgb(255, 255, 255); 
                    border: 3px solid rgb(255, 255, 255);
                }
                QPushButton:hover { 
                    border-color: rgb(253, 94, 80); 
                    color: rgb(253, 94, 80); 
                }
            """,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            font=QtGui.QFont("Hiragino Sans GB", 40, QtGui.QFont.Bold)
        )
