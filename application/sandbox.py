target = {310861551: 24, 313636312: 24, 336083842: 17, 338359049: 28, 346625887: 40, 354898042: 24, 355298478: 4, 456239474: 2, 456239599: 36, 456239600: 49, 456239602: 46, 456240749: 42, 456240810: 56, 456240938: 54, 456240956: 51, 456240986: 45, 456241098: 79}

sortx = sorted(target.items(), key=lambda x: x[1], reverse=True)[:3]

print(sortx)

for w in sortx:
    print(w[0])

target_id = '0000000'
x = [f'photo{target_id}_{v[0]}' for v in sortx]
print(x)


