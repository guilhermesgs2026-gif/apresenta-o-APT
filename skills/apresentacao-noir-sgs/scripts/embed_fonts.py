import sys,zipfile,shutil,re,os
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","fonts")
FONTS=[("Open Sauce","OpenSauce-Regular","00000500000000000000"),("Open Sauce Light","OpenSauce-Light","00000400000000000000"),("Space Mono","SpaceMono-Regular","02000509040000020004")]
def embed(src,dst):
    zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(dst,"w",zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        data=zin.read(it.filename)
        if it.filename=="[Content_Types].xml":
            t=data.decode("utf8")
            if 'Extension="fntdata"' not in t:
                t=t.replace("<Default ",'<Default Extension="fntdata" ContentType="application/x-fontdata"/><Default ',1)
            data=t.encode("utf8")
        elif it.filename=="ppt/_rels/presentation.xml.rels":
            t=data.decode("utf8")
            rel="".join(f'<Relationship Id="rIdFnt{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{i+1}.fntdata"/>' for i in range(len(FONTS)))
            t=t.replace("</Relationships>",rel+"</Relationships>"); data=t.encode("utf8")
        elif it.filename=="ppt/presentation.xml":
            t=data.decode("utf8")
            lst="<p:embeddedFontLst>"+"".join(f'<p:embeddedFont><p:font typeface="{n}" charset="1" panose="{pa}"/><p:regular r:id="rIdFnt{i+1}"/></p:embeddedFont>' for i,(n,f,pa) in enumerate(FONTS))+"</p:embeddedFontLst>"
            t=re.sub(r"(<p:notesSz [^>]*/>)",r"\1"+lst,t,count=1)
            if "embedTrueTypeFonts" not in t: t=t.replace("<p:presentation ",'<p:presentation embedTrueTypeFonts="1" ',1)
            data=t.encode("utf8")
        zout.writestr(it,data)
    for i,(n,f,pa) in enumerate(FONTS):
        zout.writestr(f"ppt/fonts/font{i+1}.fntdata",open(os.path.join(FD,f+".fntdata"),"rb").read())
    zout.close()
if __name__=="__main__": embed(sys.argv[1],sys.argv[2]); print("embedded ->",sys.argv[2])
