const { spawn } = require('child_process');

// Attach event listener for user input
process.stdout.write('$ ');
process.stdin.on('data', (data) => {
    // Remove newline character from input
    const input = data.toString().trim();

    // Split input into command and arguments
    const [ command, ...args ] = input.split(' ');


    // Execute command
    if (command === 'ls') {
      // Use spawn to execute the 'ls' command
      const ls = spawn('ls', args);

      // Print output of command
      ls.stdout.on('data', (data) => {
        process.stdout.write(data);
      });
    } else if (command === 'ps') {
      // Use spawn to execute the 'ps' command
      const ps = spawn('ps', args);

      // Print output of command
      ps.stdout.on('data', (data) => {
        process.stdout.write(data);
      });
     
    }else if (command === 'open') {
      // Use spawn to execute the 'ps' command
      //const open = spawn('open', args);
      const[ command,repo]=input.split(' ');
      try{
      const open=spawn('open',repo);
      process.stdout.write('open successful!')      
      }catch(err){
      
      process.stdout.write('Please check the repository of your file!')
      }

      // Print output of command
      //open.stdout.on('data', (data) => {
        //process.stdout.write(data);
      //});
     
    } else if (command === 'kill') {
    const [ command, option, processId ] = input.split(' ');
      if(command === 'kill' && option === '-k'){
      const kill = spawn('kill', [processId]);
      process.stdout.write(`Process with ID:${processId} killed\n`);
     }else if(command === 'kill'){
       process.stdout.write(`Invalid option ${option} for kill command\n`);
      }
     
    } else if (command === 'stop') {
     const [ command, option, processId ] = input.split(' ');
      if(command==='stop' && option === '-p'){
        // Use spawn to execute the 'kill' command with -STOP option
        const stop = spawn('kill', ['-STOP', processId]);
        process.stdout.write(`Process with ID:${processId} stopped\n`);
      } else if(command==='stop'){
        process.stdout.write(`Invalid option ${option} for stop command\n`);
      }
    } else if (command === 'cont') {
      const [, option, processId] = args
      if(option === '-c'){
        // Use spawn to execute the 'kill' command with -CONT option
        const cont = spawn('kill', ['-CONT', processId]);
        process.stdout.write(`Process with ID:${processId} continued\n`);
      }else{
        process.stdout.write(`Invalid option ${option} for continue command\n`);
      }
    } else if (command === ' exit') {
        process.stdout.write(`Exiting shell...\n`);
        process.exit(0);
    } else {
      // Invalid command
      process.stdout.write(`Invalid command\n`);
    }
    process.stdout.write('$ ');
});

