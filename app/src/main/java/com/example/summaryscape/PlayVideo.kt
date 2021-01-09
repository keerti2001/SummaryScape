    package com.example.summaryscape

import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity


class PlayVideo : AppCompatActivity() {
    var summarizedVid: VideoView? = null
    var mediaControls: MediaController? = null


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_play_video)
        summarizedVid = findViewById<View>(R.id.summarized_vid) as VideoView
        if (mediaControls == null) {
            mediaControls = MediaController(this)
            mediaControls!!.setAnchorView(this.summarizedVid)
        }

        summarizedVid!!.setMediaController(mediaControls)
        if (flag == 1) {
            summarizedVid!!.setVideoURI(Uri.parse("android.resource://" + packageName + "/" + R.raw.summarized1))
            flag = 2
        } else {
            summarizedVid!!.setVideoURI(Uri.parse("android.resource://" + packageName + "/" + R.raw.summarized2))
            flag = 1
        }
        summarizedVid!!.requestFocus()
        summarizedVid!!.start()
        summarizedVid!!.setOnCompletionListener {
            Toast.makeText(applicationContext, "Video completed",
                    Toast.LENGTH_LONG).show()
        }

        summarizedVid!!.setOnErrorListener { _, _, _ ->
            Toast.makeText(applicationContext, "An Error Occurred " + "While Playing Video !!!", Toast.LENGTH_LONG).show()
            false
        }
    }
    companion object {
        @JvmStatic var flag = 1
    }
}