package netp.raspi.surveillancesystem;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.OutputStream;
import java.io.PrintStream;
import java.net.Socket;
import java.util.ArrayList;

public class HomeScreenActivity extends Activity {

    String address;
    int portNumber;
    Button btn_record;
    ArrayList<String> arraylist_matches;
    Dialog dialog_matches;
    ListView listview_matches;
    EditText edit_socket_ip;
    EditText edit_socket_port;
    boolean showDialog = false;
    public static final int REQUEST_CODE_VOICE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_screen);
        address = "";
        portNumber = 0;
        btn_record = (Button) findViewById(R.id.home_btn_record);
        btn_record.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()) {
                    try {
                        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak Now");
                        startActivityForResult(intent, REQUEST_CODE_VOICE);
                    } catch (Exception e) {
                        Toast.makeText(getApplicationContext(), "Your phone does not support this action.", Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(getApplicationContext(), "Please connect to the Internet.", Toast.LENGTH_SHORT).show();
                }
            }
        });
        edit_socket_ip = (EditText) findViewById(R.id.socket_ip);
        edit_socket_port = (EditText) findViewById(R.id.socket_port);
    }

    @Override
    protected void onPostResume() {
        super.onPostResume();
        if (showDialog) {
            listview_matches.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    dialog_matches.hide();
                    String selected_text = arraylist_matches.get(position);
                    selected_text = selected_text.toLowerCase();
                    if (selected_text.equals("none of the above")) {
                        Dialog nomatchdialog = new Dialog(HomeScreenActivity.this);
                        nomatchdialog.setTitle(R.string.try_again_dialog);
                        nomatchdialog.setContentView(R.layout.dialog_general_layout);
                        TextView tv = (TextView) nomatchdialog.findViewById(R.id.gen_textview);
                        tv.setText(R.string.no_match);
                        nomatchdialog.show();
                    }
                    else {
                        try {
                            address = edit_socket_ip.getText().toString();
                            portNumber = Integer.valueOf(edit_socket_port.getText().toString());
                            SendSpokenTextTask task = new SendSpokenTextTask(address, portNumber);
                            task.execute(selected_text);
                        } catch (Exception e) {
                            Log.d("RASPILOG", e.toString());
                            Toast.makeText(getApplicationContext(), "Please check the address of your RasPi.", Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            });
            dialog_matches.show();
            showDialog = false;
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE_VOICE && resultCode == RESULT_OK && data != null) {
            arraylist_matches = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            arraylist_matches.add("None of the above");
            ArrayAdapter<String> adapter = new ArrayAdapter<>(HomeScreenActivity.this, android.R.layout.simple_list_item_1, android.R.id.text1, arraylist_matches);
            dialog_matches = new Dialog(HomeScreenActivity.this);
            dialog_matches.setContentView(R.layout.dialog_voice_layout);
            dialog_matches.setTitle(R.string.title_voice_dialog);
            listview_matches = (ListView) dialog_matches.findViewById(R.id.list);
            listview_matches.setAdapter(adapter);
            showDialog = true;
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    class SendSpokenTextTask extends AsyncTask<String, Void, Integer> {

        String dstAddress;
        int dstPort;

        public SendSpokenTextTask(String address, int portNumber) {
            dstAddress = address;
            dstPort = portNumber;
        }

        protected Integer doInBackground(String... params) {
            try {
                Socket socket = new Socket(dstAddress, dstPort);
                OutputStream outputStream = socket.getOutputStream();
                PrintStream printStream = new PrintStream(outputStream);
                String query = params[0];
                String len = query.length() + "";
                printStream.print(len);
                printStream.print(query);
                printStream.close();
                socket.close();
            } catch (Exception e) {
                Log.d("RASPILOG", e.toString());
                e.printStackTrace();
                return 1;
            }
            return 0;
        }

        protected void onPostExecute(Integer result) {
            if (result == 0)
                Toast.makeText(getApplicationContext(), "The command has been sent.", Toast.LENGTH_SHORT).show();
            else
                Toast.makeText(getApplicationContext(), "Couldn't send the command, please try again.", Toast.LENGTH_SHORT).show();
        }
    }

    public boolean isConnected() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo net = cm.getActiveNetworkInfo();
        return (net != null && net.isAvailable() && net.isConnected());
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        super.onCreateOptionsMenu(menu);
        return true;
    }

}
