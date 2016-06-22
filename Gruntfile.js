//Gruntfile.js

module.exports = function(grunt) {

  // ===========================================================================
  // CONFIGURE GRUNT ===========================================================
  // ===========================================================================
  grunt.initConfig({

    // get the configuration info from package.json ----------------------------
    // this way we can use things like name and version (pkg.name)
    pkg: grunt.file.readJSON('package.json'),

    // configure jshint to validate js files -----------------------------------
    watch: {
      scripts: {
        files: ['**/*.vp', 'names.py'],
        tasks: ['shell'],
        options: {
          spawn: false,
        }
      }
    },
    shell: {
        options: {
            stderr: false
        },
        target: {
            command: './2english-init.py && ./2html.py && ./upload.sh'
        }
    }
  });

  // ===========================================================================
  // LOAD GRUNT PLUGINS ========================================================
  // ===========================================================================
  // we can only load these if they are in our package.json
  // make sure you have run npm install so our app can find these
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-shell');

};
