import clr

pathDLL = "C:/Users/ASUS/source/repos/Hors-master/bin/debug/netstandard2.0/Hors.dll"
clr.AddReference(pathDLL)

import Hors
from System import DateTime
recognized_text = "встреча завтра в 9"

today = DateTime.Now

parser = Hors.HorsTextParser()
result = parser.Parse(recognized_text, today, 4)

print(result.Text)

fdate = result.Dates[0]
#fdate.Type - fixed or not
#fdate.DateFrom - начало
#fdate.DateTo - конец
#fdate.Span - формат времени?
#fdate.HasTime - t\f было ли указано время
#fdate.StartIndex - int, начало хер пойми чего
#fdate.EndIndex - the same

print(fdate.DateFrom.ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ss'+'05:00"))
print(fdate.DateTo.ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ss'+'05:00"))
