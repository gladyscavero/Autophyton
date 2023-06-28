import sbol2
import csv

class pb_component:
    roles = []
    def __init__(self, display_id, roles, sequence):
        self.display_id = display_id
        self.roles = roles
        self.sequence = sequence


ROLES = {
    "http://identifiers.org/so/SO:0000141": "terminator",
    "http://identifiers.org/so/SO:0000619": "terminator",
    "http://identifiers.org/so/SO:0000620": "terminator",
    "http://identifiers.org/so/SO:0000163": "terminator",
    "http://identifiers.org/so/SO:0000951": "terminator",
    "http://identifiers.org/so/SO:0000614": "terminator",
    "http://identifiers.org/so/SO:0000167": "promoter",
    "http://identifiers.org/so/SO:0002221": "promoter",
    "http://identifiers.org/so/SO:0002222": "promoter",
    "http://identifiers.org/so/SO:0000139": "RBS",
    "http://identifiers.org/so/SO:0000316": "CDS",
}

def main():
    igem_2018_path = "CnD_collection.xml"
    # igem_2018_path = "free_genes_feature_libraries_collection.xml"
    doc = sbol2.Document()
    doc.read(igem_2018_path)

    components = {}
    for obj in doc:
        if isinstance(obj, sbol2.ComponentDefinition):
            aux_roles = []

            for role in obj.roles:
                print(role, obj.displayId)
                aux_roles.append(ROLES.get(role))
            
            if components.get(obj.displayId) is None:
                components[obj.displayId] = (pb_component(obj.displayId, aux_roles, None))  
            else:
                components[obj.displayId].roles = aux_roles

        if isinstance(obj, sbol2.Sequence):
            seq_id = obj.displayId.replace("Sequence", "")
            if components.get(seq_id) is not None:
                components[seq_id].sequence = obj.elements 
        
    # for key, value in components.items():
    #     print(f"Component '{key}' has roles '{value.roles}' and sequence '{value.sequence}'")

    with open('components.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["display_id", "role", "sequence"])
        for key, value in components.items():
            writer.writerow([key, value.roles[0], value.sequence])


if __name__ == '__main__':
    main()
