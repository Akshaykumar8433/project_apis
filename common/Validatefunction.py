
def validateParamsFromCheckList(requestdata,checkdetail):
    output_obj = {}
    for i in checkdetail:
        if isinstance(requestdata.get(i),checkdetail.get(i)):
            output_obj[i] = requestdata.get(i)
        else:
            raise Exception("type_mismatch")

    return output_obj
