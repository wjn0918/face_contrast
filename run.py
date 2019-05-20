from faceContrast.api import app
from faceContrast.schedule import Schedule

def main():

    s = Schedule()
    s.run()
    app.run(host='',port=5001)


if __name__ == '__main__':
    main()


