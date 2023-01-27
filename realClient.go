package main
import (
	//"io"
	"os"
	"net"
	//"fmt"
)
func main(){
	conn,err:=net.Dial("tcp","localhost:8000")
	conn1,_:=net.Dial("tcp","localhost:8080")
	if err!=nil{
	panic(err)
	}
	
	im1,_:=os.Create("final.jpg")
	fi,err:=os.Open("original.jpg")
	if err!=nil{
	panic(err)
	}
	buf:=make([]byte,65000)
	//stocker le fichier dans les buffers
	for{
		n,_:=fi.Read(buf)
		if n==0{
			break
		}
		conn.Write(buf[:n])	
	}
	//fmt.Print("fini!")
	conn.Close()
	
	
	
	//receive the image
	//image1,_:=os.Open("READM.md")
	
	buff:=make([]byte,65000)
	
	
	
	
	for{
		n,_:=conn1.Read(buff)
	//	if n==0{
			//break
	//	}
		im1.Write(buff[:n])
		
		if n==0{
			break
		}
	//fmt.Print("fini!")
	}
	
	
	
		

}
