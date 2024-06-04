package com.pilet.omni.utils

import com.pilet.omni.models.MessageModel

interface NewMessageInterface {
    fun onNewMessage(message: MessageModel)
}