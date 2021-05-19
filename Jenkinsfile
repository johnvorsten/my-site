#!groovy

pipeline {
    agent any

    stages {
        stage("build") {
            steps {
                // Start. How does the message get to the console?
                echo "Starting Build"

                // Environment variables
                echo "Running ${env.BUILD_ID} ${env.BUILD_DISPLAY_NAME} on ${env.NODE_NAME} and JOB ${env.JOB_NAME}"
                echo "Running in ${env.WORKSPACE}"

                // Create a  conda environment and install dependencies
                bat "C:\\ProgramData\\Miniconda3\\Scripts\\activate.bat"
                bat "conda create --yes -n ${env.BUILD_TAG} python=3.7"
                bat "conda activate ${env.BUILD_TAG}"
                bat "pip install -q --user -r ${env.WORKSPACE}\\requirements.txt"
                bat "conda info --envs"
            }
        }

        stage("Test") {
            steps{
                // Print
                echo "Test Stage"

                // Unittest Django
                // Only test these apps = [about, jv_blog, jv_github,]
                dir('my_site') {
                    bat "python manage.py test --settings my_site.settings_test about.tests"
                    bat "python manage.py test --settings my_site.settings_test jv_blog.tests"
                    bat "python manage.py test --settings my_site.settings_test jv_github.tests"
                }
            }
        }

        stage("Deploy") {
            steps{
                echo "Deploy stage"
                // Copy files to temporary directory at /home/johnvorsten/web/temp
                sshPublisher(publishers: [sshPublisherDesc(configName: 'webserver', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: '', execTimeout: 120000, flatten: false, makeEmptyDirs: true, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '/home/johnvorsten/web/temp', remoteDirectorySDF: false, removePrefix: '', sourceFiles: 'my_site\\**\\*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true)])
                // Requirements file to webserver folder
                sshPublisher(publishers: [sshPublisherDesc(configName: 'webserver', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: '', execTimeout: 120000, flatten: false, makeEmptyDirs: true, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '/home/johnvorsten/web/temp', remoteDirectorySDF: false, removePrefix: '', sourceFiles: 'requirements.txt')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true)])
                // Environment variables will not be set from Jenkins
                // Execute the web-start.sh script on the remote server
                // sudo /home/johnvorsten/web/temp/virtual-machine/web-start.sh
                sshPublisher(publishers: [sshPublisherDesc(configName: 'webserver', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'sudo /home/johnvorsten/web/temp/my_site/virtual-machine/web-start.sh', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true)])

            }
        }

        
    } // End of stages

    post {
        always {
            echo "Removing unused conda environment"
            bat "conda env remove --yes -n ${BUILD_TAG}"
            echo "Success"
        }

        success {
            // Delete the old files in /home/johnvorsten/web/temp
            sshPublisher(publishers: [sshPublisherDesc(configName: 'webserver', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'rm -r /home/johnvorsten/web/temp', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
            echo "Success"
        }

    } // End of post

} // End of pipeline