import os
import time
import xml.dom.minidom as md


def faru(folder):
    print("Executing prepar_ilo: ")

    file_list = get_xml_files(folder)

    dom_impl = md.getDOMImplementation()
    all_files = dom_impl.createDocument(None, "all_files", None)
    top_element = all_files.documentElement

    for file in file_list:
        rows = process_file(os.path.join(folder, file))

        file_element = all_files.createElement("file")
        file_element.setAttribute("name", file)
        top_element.appendChild(file_element)

        for row in rows:
            file_element.appendChild(row)

    start_time = time.time()
    with open(os.path.join(folder, "../all_files_joined.xml"), "w") as f:
        f.write(all_files.toprettyxml())
    end_time = time.time()
    duration = (end_time - start_time) * 1000
    print(f"Write all lines: {duration:.2f} ms")


def get_xml_files(folder_name):
    """
    This function takes a folder name as input and returns a list of all files with the .xml extension.

    Args:
        folder_name: The name of the folder to search.

    Returns:
        A list of all files with the .xml extension in the folder.
    """
    print("Getting XML files from: " + folder_name)

    xml_files = []
    for filename in os.listdir(folder_name):
        if filename.endswith(".xml"):
            xml_files.append(filename)
    return xml_files


def write_list_to_file(lines, output_file):
    """
    This function takes a list of strings and writes them to a file, separated by newlines.

    Args:
        lines: A list of lines to write.
        output_file: The name of the file to write to.
    """

    print(f"writing {len(lines)} lines to file: {output_file}")

    start_time = time.time()
    with open(output_file, "w") as f:
        f.write("\n".join(lines))
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"\t write all lines: {duration:.2f} ms")


def process_file(file):
    print(f"Processing file: {file}")
    start_time = time.time()

    docs = md.parse(file)
    all_rows = []
    all_rows.extend(docs.getElementsByTagName("p"))
    all_rows.extend(docs.getElementsByTagName("head"))
    for row in all_rows:
        remove_names(row)

    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"\t Done {file}: {duration:.2f} ms")

    return all_rows


def remove_children(p, children):
    for child in children:
        parent = child.parentNode
        if parent:
            parent.removeChild(child)
    return p


def remove_names(p):
    names = p.getElementsByTagName("name")
    remove_children(p, names)
    abbrs = p.getElementsByTagName("abbr")
    remove_children(p, abbrs)
    emphs = p.getElementsByTagName("emph")
    remove_children(p, emphs)
    foreigns = p.getElementsByTagName("foreign")
    remove_children(p, foreigns)
    ptrs = p.getElementsByTagName("ptr")
    remove_children(p, ptrs)


def write_file(lines, output_file):
    with open(output_file, "w") as f:
        f.write("\n".join(lines))


def delete_addresses(file_name): 
    docs = md.parse(file_name)

    addresses = docs.getElementsByTagName("address")
    print("removing " + str(len(addresses)) + " addresses")
    remove_children(docs.documentElement, addresses)

    # titles = docs.getElementsByTagName("title")
    # print("removing " + str(len(titles)) + " titles")
    # remove_children(docs.documentElement, titles)

    with open(file_name, "w") as f:
        f.write(docs.toxml())
    
