# chatgpt-grep

A utility script designed to search for specific messages within a ChatGPT data export and to retrieve the titles of chats along with the dates of conversations containing those messages.

## Background

Navigating the nested structure of JSON in ChatGPT data exports can be challenging. This tool simplifies the process by enabling users to identify chat titles based on a keyword or phrase.

## Usage

1. Download your ChatGPT data export, which will be provided in a `.zip` file format.
2. Execute the script by specifying the path to your `.zip` file along with the target message you're searching for:

```bash
$ ./gptgrep.py path_to_your_data_export.zip "Your target message here"
```

## Features

- **Case-Insensitive Search**: Performs a case-insensitive search within messages.
- **Direct Output**: Outputs the titles and provides URL links to all chats that contain the target message.
- **Zip Extraction**: Automatically extracts data from the exported `.zip` file without manual intervention.

## Basic Usage Example

```bash
$ ./gptgrep.py ~/Downloads/a8d0cee5d7853270947c973b3be9d96370cbe76cfd7e3dc26a2714bbcddca106-2023-08-21-13-36-46.zip "my future self"
chatgpt-grep:
- date: August 22, 2023 15:52:21
  title: ChatGPT Grep
- date: August 21, 2023 09:51:02
  title: Create Pull Request from Cloned Repo
```

## Including Context Around Matches

To include additional context around matches, use the `--context` option. This option allows you to specify the number of preceding (parent) and following (child) conversation nodes included in the output. Format the option as `--context="prev,next"`, where `prev` is the number of preceding parent nodes and `next` is the number of following child nodes.

```bash
$ ./gptgrep.py --context="2,3" path_to_your_data_export.zip "Your target message here"
```

## Dependencies

- Python 3

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
