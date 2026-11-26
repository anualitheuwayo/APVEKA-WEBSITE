import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_tts/flutter_tts.dart';
import 'database_helper.dart';
import 'settings_screen.dart';

void main() {
  runApp(const VoiceNotebookApp());
}

class VoiceNotebookApp extends StatelessWidget {
  const VoiceNotebookApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice Notebook',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _controller = TextEditingController();
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;
  final stt.SpeechToText _speech = stt.SpeechToText();
  final _storage = const FlutterSecureStorage();
  final FlutterTts _flutterTts = FlutterTts();

  bool _isListening = false;
  bool _isThinking = false;

  List<Map<String, dynamic>> _notes = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadNotes();
    // Setup TTS to be ready
    _flutterTts.setLanguage("en-US");
    _flutterTts.setSpeechRate(0.5);
  }

  Future<void> _loadNotes() async {
    final data = await _dbHelper.getNotes();
    setState(() {
      _notes = data;
      _isLoading = false;
    });
  }

  Future<void> _processText() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    _controller.clear();

    if (text.startsWith('?')) {
      final question = text.substring(1).trim();
      
      await _dbHelper.insertNote('Q: $question');
      _loadNotes();

      await _askAI(question);
    } else {
      await _dbHelper.insertNote(text);
      _loadNotes();
    }
  }

  Future<void> _askAI(String question) async {
    final apiKey = await _storage.read(key: 'gemini_api_key');
    if (apiKey == null || apiKey.isEmpty) {
      _showDialog('Error', 'Please add your Gemini API Key in Settings first.');
      return;
    }

    setState(() => _isThinking = true);

    try {
      final url = Uri.parse(
          'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key=$apiKey');
      
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "system_instruction": {
            "parts": {
              "text": "You are a helpful voice assistant. You must answer in plain text only. Do NOT use markdown, do NOT use asterisks (*), do NOT use hashtags (#), and do NOT use bold text. Keep your answers short and conversational, as if you are speaking out loud."
            }
          },
          "contents": [
            {
              "parts": [
                {"text": question}
              ]
            }
          ]
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final answer = data['candidates'][0]['content']['parts'][0]['text'];
        
        await _dbHelper.insertNote('A: $answer');
        _loadNotes();

        _showDialog('AI Answer', answer);
      } else {
        _showDialog('Error', 'API Error: ${response.statusCode}\n${response.body}');
      }
    } catch (e) {
      _showDialog('Error', 'Network error: $e');
    } finally {
      setState(() => _isThinking = false);
    }
  }

  void _showDialog(String title, String content) {
    if (title == 'AI Answer') {
      // Small delay allows Chrome to finish loading the audio engine
      Future.delayed(const Duration(milliseconds: 300), () {
        _flutterTts.speak(content);
      });
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: SingleChildScrollView(child: Text(content)),
        actions: [
          TextButton(
            onPressed: () {
              _flutterTts.stop();
              Navigator.pop(context);
            },
            child: const Text('OK'),
          )
        ],
      ),
    );
  }

  Future<void> _deleteNote(int id) async {
    await _dbHelper.deleteNote(id);
    _loadNotes();
  }

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) {
            setState(() {
              _controller.text = val.recognizedWords;
            });
          },
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
      if (_controller.text.isNotEmpty) {
        _processText();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Voice Notebook'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          )
        ],
      ),
      body: Column(
        children: [
          if (_isThinking)
            const LinearProgressIndicator(),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Type a note, or ask a question starting with "?"...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _processText(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  onPressed: _listen,
                  style: IconButton.styleFrom(
                    backgroundColor: _isListening ? Colors.red : null,
                  ),
                  icon: Icon(_isListening ? Icons.stop : Icons.mic),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  onPressed: _processText,
                  icon: const Icon(Icons.add),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _notes.isEmpty
                    ? const Center(
                        child: Text('No notes yet. Speak or type above!', 
                        style: TextStyle(color: Colors.grey)),
                      )
                    : ListView.builder(
                        itemCount: _notes.length,
                        itemBuilder: (context, index) {
                          final note = _notes[index];
                          final isQuestion = note['content'].toString().startsWith('Q:');
                          final isAnswer = note['content'].toString().startsWith('A:');
                          
                          return Card(
                            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            child: ListTile(
                              leading: Icon(
                                isQuestion ? Icons.person : (isAnswer ? Icons.smart_toy : Icons.notes),
                                color: isQuestion ? Colors.blue : (isAnswer ? Colors.green : null),
                              ),
                              title: Text(
                                note['content'],
                                style: TextStyle(
                                  fontWeight: isQuestion || isAnswer ? FontWeight.bold : FontWeight.normal,
                                ),
                              ),
                              trailing: IconButton(
                                icon: const Icon(Icons.delete_outline),
                                onPressed: () => _deleteNote(note['id']),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}