// import Felgo 3.0         // a activer pour test sur smartphone
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "ADMIN : Memory Game"


    Text {
        text: "ADMIN : Memory game"
        font.bold: true
        anchors.horizontalCenter: parent.horizontalCenter

    }




    Rectangle {
            id: testTile1
            width: 80
            height: 80
            color: 'gray'
    }

}
