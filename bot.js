const allowedUsers = ['899551341263863819', '1089356674764120125'];








const Discord = require('discord.js');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const archiver = require('archiver');
const fse = require('fs-extra');

const client = new Discord.Client();

const prefix = '!';

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.on('message', async (message) => {
  if (!message.content.startsWith(prefix) || message.author.bot) return;

  const args = message.content.slice(prefix.length).trim().split(' ');
  const command = args.shift().toLowerCase();

  if (command === 'ping') {
    message.channel.send('Pong!');
  } else if (command === 'say') {
    const text = args.join(' ');
    message.channel.send(text);
  } else if (command === 'createchannel') {
    if (!allowedUsers.includes(message.author.id)) {
      message.channel.send('You are not allowed to use this command.');
      return;
    }
    const channelName = args.join(' ');

    try {
      const createdChannel = await message.guild.channels.create(channelName, {
        type: 'text',
      });

      message.channel.send(`Text channel created: ${createdChannel}`);

      // Listen to messages in the created channel
      const filter = (msg) => msg.author.id === message.author.id && msg.channel.id === createdChannel.id;
      const collector = createdChannel.createMessageCollector(filter);

      collector.on('collect', (msg) => {
        // If the user sends multiple files
        if (msg.attachments.size > 0) {
          const files = Array.from(msg.attachments.values());
          const fileNames = [];

          files.forEach((file) => {
            const filePath = path.join('skin_picture', file.name);
            fs.writeFileSync(filePath, '');
            fileNames.push(file.name);
          });

          createdChannel.send(`ได้รับคำสั่งทำมอด: ${fileNames.join(', ')} กรุณารอสักครู่จนกว่าเราจะส่งไฟล์ให้`);

          // Run the command "python mod-tool/main.py" on the terminal
          exec('python main.py', (error, stdout, stderr) => {
            if (error) {
              console.error('Error running the command:', error);
              createdChannel.send('An error occurred while running the command.');
            } else {
              console.log('Command output:', stdout);
              console.error('Command error output:', stderr);

              // Compress the file to a folder named "output"
              const outputFolder = path.join(`${message.author.id}.zip`);
              const outputZip = fs.createWriteStream(outputFolder);
              const archive = archiver('zip', {
                zlib: { level: 9 }, // Compression level: 9 (highest)
              });

              outputZip.on('close', () => {
                console.log('Archive created:', outputFolder);
                createdChannel.send('ทำมอดเสร็จแล้วโหลดมอดตรงนี้ได้เลย:', {
                  files: [outputFolder],
                });

                // Delete all files in the "skin_picture" folder
                const skinPictureFolder = path.join('skin_picture');
                fs.readdir(skinPictureFolder, (err, files) => {
                  if (err) {
                    console.error('Error reading the skin_picture folder:', err);
                    createdChannel.send('An error occurred while reading the skin_picture folder.');
                  } else {
                    files.forEach((file) => {
                      const filePath = path.join(skinPictureFolder, file);
                      fs.unlinkSync(filePath);
                    });
                    console.log('All files in skin_picture folder deleted.');

                    // Delete all files in the "skin_picture" folder
                    const modToolTaskFolder = path.join('skin_picture');
                    fs.readdir(modToolTaskFolder, (err, files) => {
                      if (err) {
                        console.error('Error reading the skin_picture folder:', err);
                        createdChannel.send('An error occurred while reading the skin_picture folder.');
                      } else {
                        files.forEach((file) => {
                          const filePath = path.join(modToolTaskFolder, file);
                          fs.unlinkSync(filePath);
                        });
                        console.log('All files in skin_picture folder deleted.');

                        // Delete the "output" folder
                        fse.removeSync('output');
                        fse.removeSync(`${message.author.id}.zip`);
                        console.log('Output folder deleted.');
                      }
                    });
                  }
                });
              });

              archive.pipe(outputZip);
              archive.directory('output/', 'output');
              archive.finalize();
            }
          });
        } else {
          // Respond to user's message
          createdChannel.send(`${msg.content}`);
        }
      });
    } catch (error) {
      console.error('Error creating channel:', error);
      message.channel.send('An error occurred while creating the channel.');
    }
  }
});

client.login('MTEyMTc2Mzc0ODAyNjI1MzM5Mg.GIoKn7.HPlEyjkoCTFT7Tgg3uYZ-CLZgHDV4ITuBvI2zk');
