list = [
    {
        "Name": "one",
        "len": 12,
    },
    {
            "Name": "two",
            "len": 20,
        },
{
            "Name": "threeo",
            "len": 5,
        },
{
            "Name": "four",
            "len": 50,
        },
{
            "Name": "asa",
            "len": 10,
        }
]


for iter_num in range(len(list)-1,0,-1):
      for idx in range(iter_num):
         if list[idx]['len']<list[idx+1]['len']:
            temp = list[idx]
            list[idx] = list[idx+1]
            list[idx+1] = temp
print(list)
