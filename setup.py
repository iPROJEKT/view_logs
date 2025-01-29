from setuptools import setup

setup(
    name='WAAMMER POST-ANALYSIS',
    options={
        'build_apps': {
            # Build asteroids.exe as a GUI application
            'gui_apps': {
                'WAAMMER POST-ANALYSIS': 'main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': 'build/logs/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.ttf',
                '**/*.dt'
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)