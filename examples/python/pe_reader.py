#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Description
# -----------
# Print information about a PE file

import lief
from lief import PE
from lief.PE import oid_to_string


from optparse import OptionParser
import sys


def print_header(binary):
    dos_header       = binary.dos_header
    header           = binary.header
    optional_header  = binary.optional_header

    format_str = "{:<33} {:<30}"
    format_hex = "{:<33} 0x{:<28x}"
    format_dec = "{:<33} {:<30d}"

    print("== Dos Header ==")
    print(format_str.format("Magic:",                       str((dos_header.magic))))
    print(format_dec.format("Used bytes in the last page:", dos_header.used_bytes_in_the_last_page))
    print(format_dec.format("File size in pages:",          dos_header.file_size_in_pages))
    print(format_dec.format("Number of relocations:",       dos_header.numberof_relocation))
    print(format_dec.format("Header size in paragraphs:",   dos_header.header_size_in_paragraphs))
    print(format_dec.format("Minimum extra paragraphs:",    dos_header.minimum_extra_paragraphs))
    print(format_dec.format("Maximum extra paragraphs",     dos_header.maximum_extra_paragraphs))
    print(format_dec.format("Initial relative SS",          dos_header.initial_relative_ss))
    print(format_hex.format("Initial SP:",                  dos_header.initial_sp))
    print(format_hex.format("Checksum:",                    dos_header.checksum))
    print(format_dec.format("Initial IP:",                  dos_header.initial_ip))
    print(format_dec.format("Initial CS:",                  dos_header.initial_relative_cs))
    print(format_hex.format("Address of relocation table:", dos_header.addressof_relocation_table))
    print(format_dec.format("Overlay number:",              dos_header.overlay_number))
    print(format_dec.format("OEM ID:",                      dos_header.oem_id))
    print(format_dec.format("OEM information",              dos_header.oem_info))
    print(format_hex.format("Address of optional header:",  dos_header.addressof_new_exeheader))
    print("")

    print("== Header ==")

    char_str = " - ".join([str(chara).split(".")[-1] for chara in header.characteristics_list])

    print(format_str.format("Signature:",               "".join(map(chr, header.signature))))
    print(format_str.format("Machine:",                 str(header.machine)))
    print(format_dec.format("Number of sections:",      header.numberof_sections))
    print(format_dec.format("Time Date stamp:",         header.time_date_stamps))
    print(format_dec.format("Pointer to symbols:",      header.pointerto_symbol_table))
    print(format_dec.format("Number of symbols:",       header.numberof_symbols))
    print(format_dec.format("Size of optional header:", header.sizeof_optional_header))
    print(format_str.format("Characteristics:",         char_str))
    print("")


    dll_char_str = " - ".join([str(chara).split(".")[-1] for chara in optional_header.dll_characteristics_lists])
    subsystem_str = str(optional_header.subsystem).split(".")[-1]
    print("== Optional Header ==")
    magic = "PE32" if optional_header.magic == PE.PE_TYPE.PE32 else "PE64"
    print(format_str.format("Magic:", magic))
    print(format_dec.format("Major linker version:",           optional_header.major_linker_version))
    print(format_dec.format("Minor linker version:",           optional_header.minor_linker_version))
    print(format_dec.format("Size of code:",                   optional_header.sizeof_code))
    print(format_dec.format("Size of initialized data:",       optional_header.sizeof_initialized_data))
    print(format_dec.format("Size of uninitialized data:",     optional_header.sizeof_uninitialized_data))
    print(format_hex.format("Entry point:",                    optional_header.addressof_entrypoint))
    print(format_hex.format("Base of code:",                   optional_header.baseof_code))
    if magic == "PE32":
        print(format_hex.format("Base of data",                optional_header.baseof_data))
    print(format_hex.format("Image base:",                     optional_header.imagebase))
    print(format_hex.format("Section alignment:",              optional_header.section_alignment))
    print(format_hex.format("File alignment:",                 optional_header.file_alignment))
    print(format_dec.format("Major operating system version:", optional_header.major_operating_system_version))
    print(format_dec.format("Minor operating system version:", optional_header.minor_operating_system_version))
    print(format_dec.format("Major image version:",            optional_header.major_image_version))
    print(format_dec.format("Minor image version:",            optional_header.minor_image_version))
    print(format_dec.format("Major subsystem version:",        optional_header.major_subsystem_version))
    print(format_dec.format("Minor subsystem version:",        optional_header.minor_subsystem_version))
    print(format_dec.format("WIN32 version value:",            optional_header.win32_version_value))
    print(format_hex.format("Size of image:",                  optional_header.sizeof_image))
    print(format_hex.format("Size of headers:",                optional_header.sizeof_headers))
    print(format_hex.format("Checksum:",                       optional_header.checksum))
    print(format_str.format("Subsystem:",                      subsystem_str))
    print(format_str.format("DLL Characteristics:",            dll_char_str))
    print(format_hex.format("Size of stack reserve:",          optional_header.sizeof_stack_reserve))
    print(format_hex.format("Size of stack commit:",           optional_header.sizeof_stack_commit))
    print(format_hex.format("Size of heap reserve:",           optional_header.sizeof_heap_reserve))
    print(format_hex.format("Size of heap commit:",            optional_header.sizeof_heap_commit))
    print(format_dec.format("Loader flags:",                   optional_header.loader_flags))
    print(format_dec.format("Number of RVA and size:",         optional_header.numberof_rva_and_size))
    print("")

def print_data_directories(binary):
    data_directories = binary.data_directories

    print("== Data Directories ==")
    f_title = "|{:<24} | {:<10} | {:<10} | {:<8} |"
    f_value = "|{:<24} | 0x{:<8x} | 0x{:<8x} | {:<8} |"
    print(f_title.format("Type", "RVA", "Size", "Section"))

    for directory in data_directories:
        section_name = directory.section.name if directory.has_section else ""
        print(f_value.format(str(directory.type).split('.')[-1], directory.rva, directory.size, section_name))
    print("")


def print_sections(binary):
    sections = binary.sections

    print("== Sections  ==")
    f_title = "|{:<10} | {:<16} | {:<16} | {:<18} | {:<16} | {:<9} | {:<9}"
    f_value = "|{:<10} | 0x{:<14x} | 0x{:<14x} | 0x{:<16x} | 0x{:<14x} | {:<9.2f} | {:<9}"
    print(f_title.format("Name", "Offset", "Size", "Virtual Address", "Virtual size", "Entropy", "Flags"))

    for section in sections:
        flags = ""
        for flag in section.characteristics_lists:
            flags += str(flag).split(".")[-1] + " "
        print(f_value.format(section.name, section.offset, section.size, section.virtual_address, section.virtual_size, section.entropy, flags))
    print("")


def print_symbols(binary):
    symbols = binary.symbols
    if len(symbols) > 0:
        print("== Symbols ==")
        f_title = "|{:<20} | {:<10} | {:<8} | {:<8} | {:<8} | {:<13} |"
        f_value = u"|{:<20} | 0x{:<8x} | {:<14} | {:<10} | {:<12} | {:<13} |"

        print(f_title.format("Name", "Value", "Section number", "Basic type", "Complex type", "Storage class"))
        for symbol in symbols:
            section_nb_str = ""
            if symbol.section_number <= 0:
                section_nb_str = str(PE.SYMBOL_SECTION_NUMBER(symbol.section_number)).split(".")[-1]
            else:
                try:
                    section_nb_str = symbol.section.name
                except:
                    section_nb_str = "section<{:d}>".format(symbol.section_number)


            print(f_value.format(
                symbol.name[:20],
                symbol.value,
                section_nb_str,
                str(symbol.base_type).split(".")[-1],
                str(symbol.complex_type).split(".")[-1],
                str(symbol.storage_class).split(".")[-1]))

def print_imports(binary):
    if binary.has_imports:
        print("== Imports ==")
        imports = binary.imports

        for import_ in imports:
            print(import_.name)
            entries = import_.entries
            f_value = "  {:<33} 0x{:<14x} 0x{:<14x} 0x{:<16x}"
            for entry in entries:
                print(f_value.format(entry.name, entry.data, entry.iat_value, entry.hint))
        print("")

def print_tls(binary):
    format_str = "{:<33} {:<30}"
    format_hex = "{:<33} 0x{:<28x}"
    format_dec = "{:<33} {:<30d}"
    if not binary.has_tls:
        return

    print("== TLS ==")
    tls = binary.tls
    callbacks = tls.callbacks
    print(format_hex.format("Address of callbacks:", tls.addressof_callbacks))
    if len(callbacks) > 0:
        print("Callbacks:")
        for callback in callbacks:
            print("  " + hex(callback))

    print(format_hex.format("Address of index:",  tls.addressof_index))
    print(format_hex.format("Size of zero fill:", tls.sizeof_zero_fill))
    print("{:<33} 0x{:<10x} 0x{:<10x}".format("Address of raw data:",
        tls.addressof_raw_data[0], tls.addressof_raw_data[1]))
    print(format_hex.format("Size of raw data:",  len(tls.data_template)))
    print(format_hex.format("Characteristics:",   tls.characteristics))
    print(format_str.format("Section:",           tls.section.name))
    print(format_str.format("Data directory:",    str(tls.directory.type)))
    print("")

def print_relocations(binary):
    if binary.has_relocations:
        relocations = binary.relocations
        print("== Relocations ==")
        for relocation in relocations:
            entries = relocation.entries
            print(hex(relocation.virtual_address))
            for entry in entries:
                print("  0x{:<8x} {:<8}".format(entry.position, str(entry.type).split(".")[-1]))
        print("")

def print_export(binary):
    if binary.has_exports:
        print("== Exports ==")
        exports = binary.get_export()
        entries = exports.entries
        f_value = "{:<20} 0x{:<10x} 0x{:<10x} 0x{:<6x} 0x{:<6x} 0x{:<10x}"
        print(f_value.format(exports.name, exports.export_flags, exports.timestamp, exports.major_version, exports.minor_version, exports.ordinal_base))
        for entry in entries:
            extern = "[EXTERN]" if entry.is_extern else ""
            print("  {:<20} 0x{:<6x} 0x{:<10x} {:<13}".format(entry.name[:20], entry.ordinal, entry.address, extern))
        print("")


def print_debug(binary):
    format_str = "{:<33} {:<30}"
    format_hex = "{:<33} 0x{:<28x}"
    format_dec = "{:<33} {:<30d}"

    if binary.has_debug:
        debug = binary.debug
        print("== Debug ==")
        print(format_hex.format("Characteristics:",     debug.characteristics))
        print(format_hex.format("Timestamp:",           debug.timestamp))
        print(format_dec.format("Major version:",       debug.major_version))
        print(format_dec.format("Minor version:",       debug.minor_version))
        print(format_str.format("type:",                str(debug.type).split(".")[-1]))
        print(format_hex.format("Size of data:",        debug.sizeof_data))
        print(format_hex.format("Address of raw data:", debug.addressof_rawdata))
        print(format_hex.format("Pointer to raw data:", debug.pointerto_rawdata))
        print("")

def print_signature(binary):
    format_str = "{:<33} {:<30}"
    format_hex = "{:<33} 0x{:<28x}"
    format_dec = "{:<33} {:<30d}"

    if not binary.has_signature:
        return

    signature = binary.signature
    print("== Signature ==")
    print(format_dec.format("Version:",          signature.version))
    print(format_str.format("Digest Algorithm:", oid_to_string(signature.digest_algorithm)))
    print("")

    print("-- Content Info --")
    content_info = signature.content_info
    print(format_str.format("Content Type:",     oid_to_string(content_info.content_type)))
    print(format_str.format("Type:",             oid_to_string(content_info.type)))
    print(format_str.format("Digest Algorithm:", oid_to_string(content_info.digest_algorithm)))
    print("")

    print("-- Certificates --")
    certificates = signature.certificates

    for crt in certificates:
        sn_str = ":".join(map(lambda e : "{:02x}".format(e), crt.serial_number))
        valid_from_str = "-".join(map(str, crt.valid_from[:3])) + " " + ":".join(map(str, crt.valid_from[3:]))
        valid_to_str = "-".join(map(str, crt.valid_to[:3])) + " " + ":".join(map(str, crt.valid_to[3:]))
        print(format_dec.format("Version:",             crt.version))
        print(format_str.format("Serial Number:",       sn_str))
        print(format_str.format("Signature Algorithm:", oid_to_string(crt.signature_algorithm)))
        print(format_str.format("Valid from:",          valid_from_str))
        print(format_str.format("Valid to:",            valid_to_str))
        print(format_str.format("Issuer:",              crt.issuer))
        print(format_str.format("Subject:",             crt.subject))
        print("")

    print("-- Signer Info --")
    signer_info = signature.signer_info
    issuer_str = " ".join(map(lambda e : oid_to_string(e[0]) + " = " + e[1], signer_info.issuer[0]))
    print(format_dec.format("Version:",             signer_info.version))
    print(format_str.format("Issuer:",              issuer_str))
    print(format_str.format("Digest Algorithm:",    oid_to_string(signer_info.digest_algorithm)))
    print(format_str.format("Signature algorithm:", oid_to_string(signer_info.signature_algorithm)))
    #print(format_str.format("Program name:",       signer_info.authenticated_attributes.program_name))
    print(format_str.format("Url:",                 signer_info.authenticated_attributes.more_info))
    print("")


def main():
    optparser = OptionParser(
            usage='Usage: %prog [options] <pe-file>',
            add_help_option = True,
            prog=sys.argv[0])

    optparser.add_option('-a', '--all',
            action='store_true', dest='show_all',
            help='Show all informations')

    optparser.add_option('-d', '--data-directories',
            action='store_true', dest='show_data_directories',
            help='Display data directories')

    optparser.add_option('--debug',
            action='store_true', dest='show_debug',
            help='Display debug directory')

    optparser.add_option('-g', '--signature',
            action='store_true', dest='show_signature',
            help="Display the binary's signature if any")

    optparser.add_option('-H', '--header',
            action='store_true', dest='show_headers',
            help='Display headers')

    optparser.add_option('-i', '--import',
            action='store_true', dest='show_imports',
            help='Display imported functions and libraries')

    optparser.add_option('-r', '--relocs',
            action='store_true', dest='show_relocs',
            help='Display the relocations (if present)')

    optparser.add_option('-S', '--section-headers', '--sections',
            action='store_true', dest='show_section_header',
            help="Display the sections' headers")

    optparser.add_option('-s', '--symbols', '--syms',
            action='store_true', dest='show_symbols',
            help='Display symbols')

    optparser.add_option('-t', '--tls',
            action='store_true', dest='show_tls',
            help='Display TLS informations')

    optparser.add_option('-x', '--export',
            action='store_true', dest='show_export',
            help='Display exported functions/libraries')



    options, args = optparser.parse_args()

    if len(args) == 0:
        optparser.print_help()
        sys.exit(1)

    binary = None
    try:
        binary = PE.parse(args[0])
    except lief.exception as e:
        print(e)
        sys.exit(1)


    if options.show_data_directories or options.show_all:
        print_data_directories(binary)

    if options.show_headers or options.show_all:
        print_header(binary)

    if options.show_imports or options.show_all:
        print_imports(binary)

    if options.show_relocs or options.show_all:
        print_relocations(binary)

    if options.show_section_header or options.show_all:
        print_sections(binary)

    if options.show_symbols or options.show_all:
        print_symbols(binary)

    if options.show_tls or options.show_all:
        print_tls(binary)

    if options.show_export or options.show_all:
        print_export(binary)

    if options.show_debug or options.show_all:
        print_debug(binary)

    if options.show_signature or options.show_all:
        print_signature(binary)

if __name__ == "__main__":
    main()
