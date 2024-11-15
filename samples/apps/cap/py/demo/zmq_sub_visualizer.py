import sys
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
from typing import Dict, List, Optional

import _paths  # noqa
import zmq
from autogencap.config import xpub_url
from autogencap.debug_log import Debug, Error, Info

# Import all protobuf message types
from autogencap.proto.CAP_pb2 import (
    ActorInfo, ActorInfoCollection, ActorLookup, ActorLookupResponse,
    ActorRegistration, Error as ProtoError, Ping, Pong
)
from autogencap.proto.Autogen_pb2 import (
    DataMap, GenReplyReq, GenReplyResp, PrepChat, ReceiveReq, Terminate
)


class MessageVisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Teams Runtime Message Visualizer")
        self.root.geometry("1200x800")
        
        # Configure default font
        default_font = ('Segoe UI', 10)
        heading_font = ('Segoe UI', 10, 'bold')
        
        # Configure styles
        style = ttk.Style()
        style.configure('Treeview', font=default_font)
        style.configure('Treeview.Heading', font=heading_font)
        
        # Configure alternating colors
        style.configure('Treeview', 
                       background='#f0f0f0',
                       fieldbackground='#f0f0f0')
        style.map('Treeview',
                 background=[('selected', '#0078D7')])
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="5")
        self.main_container.grid(row=0, column=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create filter frame
        self.filter_frame = ttk.Frame(self.main_container)
        self.filter_frame.grid(row=0, column=0, sticky=(W, E), pady=5)
        
        # Filter entry
        ttk.Label(self.filter_frame, text="Filter Topic:").pack(side=LEFT, padx=5)
        self.filter_var = StringVar()
        self.filter_entry = ttk.Entry(self.filter_frame, textvariable=self.filter_var)
        self.filter_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        
        # Filter buttons
        ttk.Button(self.filter_frame, text="Apply Filter", 
                  command=self.apply_filter).pack(side=LEFT, padx=5)
        ttk.Button(self.filter_frame, text="Clear Filter", 
                  command=self.clear_filter).pack(side=LEFT, padx=5)
        ttk.Button(self.filter_frame, text="Clear Messages", 
                  command=self.clear_messages).pack(side=LEFT, padx=5)

        # Create paned window for resizable panels
        self.paned = ttk.PanedWindow(self.main_container, orient=HORIZONTAL)
        self.paned.grid(row=1, column=0, sticky=(N, W, E, S))
        self.main_container.rowconfigure(1, weight=1)
        self.main_container.columnconfigure(0, weight=1)

        # Create message list and details within paned window
        self.create_message_list()
        self.create_message_details()

        # Initialize ZMQ
        self.visualizer = MessageVisualizer(self)
        
        # Start ZMQ thread
        self.zmq_thread = threading.Thread(target=self.visualizer.run, daemon=True)
        self.zmq_thread.start()

    def create_message_list(self):
        """Create the message list view"""
        # Message list frame
        list_frame = ttk.LabelFrame(self.paned, text="Messages", padding="5")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Create treeview
        self.tree = ttk.Treeview(list_frame, columns=('Time', 'Sender', 'Receiver', 'Type'), 
                                show='headings', selectmode='browse')
        
        # Configure columns
        self.tree.heading('Time', text='Time')
        self.tree.heading('Sender', text='Sender')
        self.tree.heading('Receiver', text='Receiver')
        self.tree.heading('Type', text='Type')
        
        self.tree.column('Time', width=100)
        self.tree.column('Sender', width=150)
        self.tree.column('Receiver', width=150)
        self.tree.column('Type', width=100)

        # Configure tag for alternating rows
        self.tree.tag_configure('oddrow', background='#E8E8E8')
        self.tree.tag_configure('evenrow', background='#FFFFFF')

        # Add scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid all elements
        self.tree.grid(row=0, column=0, sticky=(N, W, E, S))
        vsb.grid(row=0, column=1, sticky=(N, S))
        hsb.grid(row=1, column=0, sticky=(E, W))

        # Add frame to paned window
        self.paned.add(list_frame, weight=3)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def create_message_details(self):
        """Create the message details view"""
        # Details frame
        details_frame = ttk.LabelFrame(self.paned, text="Message Details", padding="5")
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)

        # Create a custom style for the Text widget with brighter colors
        details_style = {
            'font': ('Consolas', 11),
            'background': '#1E1E1E',  # Darker background for better contrast
            'foreground': '#FFFFFF',  # Bright white for default text
            'insertbackground': '#FFFFFF',  # White cursor
            'selectbackground': '#264F78',  # Brighter selection background
            'selectforeground': '#FFFFFF',  # White selected text
            'spacing1': 0,  # No spacing above paragraphs
            'spacing2': 0,  # No spacing between paragraphs
            'spacing3': 0,  # No spacing below paragraphs
            'padx': 5,      # Minimal horizontal padding
            'pady': 5       # Minimal vertical padding
        }

        # Details text with custom styling
        self.details_text = Text(details_frame, wrap=WORD, **details_style)
        self.details_text.grid(row=0, column=0, sticky=(N, W, E, S))
        
        # Configure tags for syntax highlighting with brighter colors
        self.details_text.tag_configure('key', foreground='#FF8C00')      # Bright orange for keys
        self.details_text.tag_configure('value', foreground='#90EE90')    # Light green for values
        self.details_text.tag_configure('number', foreground='#87CEEB')   # Sky blue for numbers
        self.details_text.tag_configure('header', foreground='#FFD700', font=('Consolas', 11, 'bold'))  # Gold for headers
        
        # Scrollbar with custom style
        details_vsb = ttk.Scrollbar(details_frame, orient="vertical", 
                                   command=self.details_text.yview)
        details_vsb.grid(row=0, column=1, sticky=(N, S))
        self.details_text.configure(yscrollcommand=details_vsb.set)

        # Add frame to paned window
        self.paned.add(details_frame, weight=2)

    def add_message(self, message: Dict):
        """Add a message to the tree view"""
        self.root.after(0, self._add_message, message)

    def _add_message(self, message: Dict):
        """Internal method to add message (called from main thread)"""
        # Get current number of items to determine odd/even
        item_count = len(self.tree.get_children())
        
        # Create combined tags list - payload and row color
        tags = [message['payload'], 'evenrow' if item_count % 2 == 0 else 'oddrow']
        
        # Insert with both payload and row color tags
        item = self.tree.insert('', 'end', values=(
            message['timestamp'],
            message['sender'],
            message['topic'],  # 'topic' represents the receiver in the message
            message['type']
        ), tags=tags)
        
        self.tree.see(item)  # Scroll to show new item

    def on_select(self, event):
        """Handle selection of message in tree view"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # Get the payload from the first tag
        item = selected_items[0]
        payload = self.tree.item(item)['tags'][0]  # First tag is always payload
        
        # Update details view
        self.details_text.delete('1.0', END)
        
        # Apply basic syntax highlighting
        try:
            # Split the payload into lines
            lines = payload.split('\n')
            for line in lines:
                # Handle key-value pairs
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    self.details_text.insert(END, key + ': ', 'key')
                    
                    # Check if value is a number
                    if value.replace('.', '').isdigit():
                        self.details_text.insert(END, value + '\n', 'number')
                    else:
                        self.details_text.insert(END, value + '\n', 'value')
                else:
                    # Check if line looks like a header (all caps or starts with ---)
                    if line.isupper() or line.startswith('---'):
                        self.details_text.insert(END, line + '\n', 'header')
                    else:
                        self.details_text.insert(END, line + '\n')
        except Exception:
            # If any error occurs during highlighting, just insert the plain text
            self.details_text.delete('1.0', END)
            self.details_text.insert('1.0', payload)

    def apply_filter(self):
        """Apply the filter from the entry field"""
        filter_text = self.filter_var.get()
        if filter_text:
            self.visualizer.set_filter(filter_text)

    def clear_filter(self):
        """Clear the current filter"""
        self.filter_var.set("")
        self.visualizer.clear_filter()

    def clear_messages(self):
        """Clear all messages from the tree view"""
        self.tree.delete(*self.tree.get_children())
        self.details_text.delete('1.0', END)


class MessageVisualizer:
    def __init__(self, gui: MessageVisualizerGUI):
        self.gui = gui
        
        # Initialize ZMQ context and socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.connect(xpub_url)
        
        # Message type mapping
        self.proto_types = {
            # CAP messages
            'ActorInfo': ActorInfo,
            'ActorInfoCollection': ActorInfoCollection,
            'ActorLookup': ActorLookup,
            'ActorLookupResponse': ActorLookupResponse,
            'ActorRegistration': ActorRegistration,
            'Error': ProtoError,
            'Ping': Ping,
            'Pong': Pong,
            # Autogen messages
            'DataMap': DataMap,
            'GenReplyReq': GenReplyReq,
            'GenReplyResp': GenReplyResp,
            'PrepChat': PrepChat,
            'ReceiveReq': ReceiveReq,
            'Terminate': Terminate
        }

        self.filter_topic: Optional[str] = None
        self.running = True
        self.subscribe_all()

    def subscribe_all(self):
        """Subscribe to all messages"""
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        Debug("VISUALIZER", "Subscribed to all messages")

    def set_filter(self, topic: str):
        """Set topic filter for display"""
        self.filter_topic = topic
        Info("VISUALIZER", f"Filter set to: {topic}")

    def clear_filter(self):
        """Clear topic filter"""
        self.filter_topic = None
        Info("VISUALIZER", "Filter cleared")

    def process_message(self) -> Optional[Dict]:
        """Process a single message"""
        try:
            # Receive multipart message
            multipart_msg = self.socket.recv_multipart()
            
            # Decode message parts
            topic = multipart_msg[0].decode('utf-8')
            msg_type = multipart_msg[1].decode('utf-8')
            sender = multipart_msg[2].decode('utf-8')
            payload = multipart_msg[3]

            # Parse payload based on message type
            if msg_type in self.proto_types:
                proto_msg = self.proto_types[msg_type]()
                try:
                    proto_msg.ParseFromString(payload)
                    payload_str = str(proto_msg)
                except Exception as e:
                    payload_str = f"Error parsing {msg_type}: {e}"
            else:
                try:
                    payload_str = payload.decode('utf-8')
                except UnicodeDecodeError:
                    payload_str = f"<binary data of length {len(payload)}>"

            # Create message record
            message = {
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                'topic': topic,
                'type': msg_type,
                'sender': sender,
                'payload': payload_str
            }

            # Return message if it matches filter
            if not self.filter_topic or self.filter_topic in topic:
                return message

        except zmq.Again:
            return None
        except Exception as e:
            Error("VISUALIZER", f"Error processing message: {e}")
            return None

    def run(self):
        """Main loop to receive and display messages"""
        try:
            while self.running:
                message = self.process_message()
                if message:
                    self.gui.add_message(message)
        except Exception as e:
            Error("VISUALIZER", f"Error in message loop: {e}")
        finally:
            self.socket.close()
            self.context.term()


def main():
    root = Tk()
    app = MessageVisualizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
