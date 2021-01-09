package com.example.summaryscape

import android.annotation.SuppressLint
import android.app.ProgressDialog
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import com.android.volley.Request
import com.android.volley.RetryPolicy
import com.android.volley.VolleyError
import com.android.volley.toolbox.Volley
import java.io.FileOutputStream


class MainActivity : AppCompatActivity() {
    private lateinit var etYTLink:EditText
    private lateinit var btnSummary:CardView
    /* Put your IP:Port here of where your Flask backend is running */
    private var backendIP = "http://192.168.1.6"
    @SuppressLint("ShowToast")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        etYTLink = findViewById(R.id.et_yt_link)
        btnSummary = findViewById(R.id.btn_summary)
        val progressDialog = ProgressDialog(this)
        progressDialog.setMessage("Processing the video...")

        btnSummary.setOnClickListener {
            Log.d("Button", "Clicked")
            val rootView = it.rootView

            if (etYTLink.text.isNotEmpty()) {

                progressDialog.show()

                // Instantiate the RequestQueue.
                val queue = Volley.newRequestQueue(this)
                val serverURL = backendIP + "/?link=" + etYTLink.text.toString()
                Log.d("Inside", serverURL)

                val request = InputStreamVolleyRequest(Request.Method.GET, serverURL,
                        { response ->
                            // TODO handle the response
                            try {
                                val outputStream: FileOutputStream
                                val name = "reference.mp4"
                                outputStream = openFileOutput(name, Context.MODE_PRIVATE)
                                outputStream.write(response)
                                Log.d("Ooutput", response.toString())
                                outputStream.close()
                                Log.d("Status", "Download complete.")
                                progressDialog.dismiss()
                                val intent = Intent(this, PlayVideo :: class.java)
                                startActivity(intent)
                            } catch (e: Exception) {
                                // TODO Auto-generated catch block
                                Log.d("KEY_ERROR", "UNABLE TO DOWNLOAD FILE")
                                e.printStackTrace()
                            }
                        }, { error -> // TODO handle the error
                    error.printStackTrace()
                }, null)
                request.retryPolicy = object : RetryPolicy {
                    override fun getCurrentTimeout(): Int {
                        return 50000
                    }

                    override fun getCurrentRetryCount(): Int {
                        return 50000
                    }

                    @Throws(VolleyError::class)
                    override fun retry(error: VolleyError) {
                    }
                }
                queue.add(request)

            } else {
                Toast.makeText(this, "Please enter the link!", Toast.LENGTH_LONG)
            }
        }


    }
}