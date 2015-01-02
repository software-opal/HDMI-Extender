from distutils.core import setup

setup(name='HDMI-parser',
      version='0.1',
      description='A set of python scripts used to capture HDMI packets over a network',
      author='Lee Symes',
      author_email='leesdolphin@gmail.com',
      url='https://github.com/leesdolphin/HDMI-Extender/',
      install_requires=["av", "pillow"], # And opencv - but we can't install it using pip.
      scripts=['handshaker.py', 'main-audio-cap.py', 'main-video-cap.py']
     )
