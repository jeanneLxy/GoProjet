package main
import (
	"fmt"
	"net"
	"io/ioutil"
	"image"
	"image/jpeg"
)
func main(){
	//definir l'@ ip et le port
	addr,_:=net.ResolveTCPAddr("tcp","127.0.0.1:1234")

	//connexion au serveur
	conn,_:=net.DialTCP("tcp",nil,addr)

	data,_:=ioutil.ReadFile("original.jpg")
	conn.Write(data)
	//réception de données
	n,_:=conn.Read(data)
	newFile1,_:=os.Create("gray.jpg")
	defer newFile1.Close()
	jepg.Encode(newFile1,data,&jpeg.Options{Quality:100})


}
